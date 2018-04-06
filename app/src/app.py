import multiprocessing as mp
from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
import numpy as np
import time
from collections import defaultdict, OrderedDict, Counter
from app.src import model_utils as mu
from app.src import multiprocessing_utils as mpu
from app.src import collection_utils as cu
from app.src import aggregation, input_output, logger_factory
from app.src.adapter import clustering_dict_to_json
from app.src.clustering import create_cluster_context_sink

log_factory = logger_factory.LoggerFactory()
app_logger = log_factory.instance(__name__)

def app_get_json_inputs(docs_folder, hashes_folder):
    source_jsons = input_output.get_jsons_from_folder(docs_folder)
    hash_jsons = input_output.get_jsons_from_folder(hashes_folder)
    return (source_jsons, hash_jsons)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def app_create_categories_from_clustering(cluster_context,
                                          documents,
                                          document_hashes_by_hashes,
                                          queue, sample_size = 5000):
    categories = defaultdict(dict)
    vectorizer = cluster_context.vectorizer
    svd =  cluster_context.svd
    used_categories = set()
    # d_chunks = chunks(documents, 1000)

    import random
    sample = random.sample(documents, sample_size)
    iter = 0
    app_logger.info(f"predicting categories with a sample size of {sample_size}")
    start_time = time.time()
    streaming_avg_lsa = None
    labels = set(cluster_context.cluster_model.labels_)

    for document in sample:
        document_vector = vectorizer.transform(document.vector_dict()) # .vector_dict()
        if svd is not None:
            lsa_time = time.time()
            dense_vector = svd.transform(document_vector)
            document_vector = dense_vector
            lsa_time = time.time() - lsa_time
            if streaming_avg_lsa is None:
                streaming_avg_lsa = lsa_time
            else:
                streaming_avg_lsa = (streaming_avg_lsa + lsa_time) / 2
        # Prediction is cluster id which is from ([-1]) [0] ... [n]
        prediction = str(cluster_context.predict(document_vector))
        category = document_hashes_by_hashes[document.id][0].category()
        if prediction not in categories:
            categories[prediction] = Counter()
        used_categories.add(category)
        categories[prediction][category] += 1
        iter += 1
        if(iter %(sample_size/10)==0):
            pos = f"{iter}/{sample_size}"
            time_elapsed = (time.time() - start_time) * 1000
            if streaming_avg_lsa is not None:
                app_logger.info(f"average time for LSA transform is {round(streaming_avg_lsa * 1000)} ms")
            app_logger.info(f"{pos} done for modelling, time elapsed {round(time_elapsed)} ms")

    cu.fill_labels(categories, labels, used_categories)
    # Add zeroes for all categories so results are equal size
    cu.fill_counters(categories, used_categories)

    # Sort by categories which are from 0 .. n
    sorting = sorted(categories.items(), key=lambda t: t[0])
    sorted_dict = OrderedDict(sorting)
    # Put (id, dict) to queue
    queue.put((cluster_context, sorted_dict))


def app_do_clustering(documents_by_strategies, document_hashes_by_hashes, cluster_contexts, queue):
    processes = []
    for cluster_context in cluster_contexts:
        documents = documents_by_strategies[cluster_context.id]
        p = mpu.create_process_and_start(app_create_categories_from_clustering,
                                         (cluster_context, documents, document_hashes_by_hashes, queue),
                                         app_logger.info(f"Started {cluster_context.id} clustering"))
        processes.append(p)
    return processes


def app_create_cluster_context(num_clusters, models_output, documents_by_strategies, queue):
    """"""
    processes = []
    for (strategy, documents) in documents_by_strategies.items():
        p = mpu.create_process_and_start(create_cluster_context_sink,
                                         (num_clusters, models_output, strategy, documents, queue),
                                         app_logger.info(f"Started {strategy} cluster context modelling"))
        processes.append(p)
    return processes


def app_create_cluster_context_worker(num_clusters, models_output, documents_by_strategies):
    queue = mp.Queue()
    processes = app_create_cluster_context(num_clusters, models_output, documents_by_strategies, queue)
    cluster_contexts = mpu.gather_to_list_and_join(queue, processes)
    queue.close()
    return cluster_contexts


def app_do_clustering_worker(documents_by_strategies, document_hashes_by_hashes, cluster_context):
    queue = mp.Queue()
    processes = app_do_clustering(documents_by_strategies, document_hashes_by_hashes, cluster_context, queue)
    categories_by_clusters = mpu.gather_to_dict_from_clustering_context_and_dict_and_join(queue, processes)
    queue.close()
    return categories_by_clusters


def app_clustering_worker(num_clusters, models_output, documents_by_strategies, document_hashes_by_hashes):
    cluster_contexts = app_create_cluster_context_worker(num_clusters, models_output, documents_by_strategies)
    categories_by_clusters = app_do_clustering_worker(documents_by_strategies, document_hashes_by_hashes,
                                                      cluster_contexts)
    return categories_by_clusters


def do_grouping_sink(id, attribute, combiner, jsons, queue):
    """
    :param id: how the result is tied up in tuple as (id, result)
    :param attribute: attribute of object-class to group by
    :param combiner: way to turn json to some kind of model (object-class)
    :param jsons: json collection
    :param queue: sink to store the result
    :return:
    """
    result = aggregation.group_by_attribute(combiner(jsons), attribute)
    queue.put((id, result))


def app_grouping_worker(source_jsons, hash_jsons):
    queue = mp.Queue()

    dbs_id, dbh_id, dhbh_id = 'documents_by_strategies', 'documents_by_hashes', 'document_hashes_by_hashes'

    p_dbs = mpu.create_process_and_start(do_grouping_sink,
                                         (dbs_id, 'strategy', mu.document_combiner,
                                          source_jsons, queue),
                                         app_logger.info(f"Started grouping with id: {dbs_id}"))

    p_dbh = mpu.create_process_and_start(do_grouping_sink,
                                         (dbh_id, 'id', mu.document_combiner,
                                          source_jsons, queue),
                                         app_logger.info(f"Started grouping with id: {dbh_id}"))

    p_dhbh = mpu.create_process_and_start(do_grouping_sink,
                                          (dhbh_id, 'id', mu.document_hash_combiner,
                                           hash_jsons, queue),
                                          app_logger.info(f"Started grouping with id: {dhbh_id}"))

    results = mpu.gather_to_dict_from_tuples_and_join(queue, [p_dbs, p_dbh, p_dhbh])
    queue.close()
    return results[dbs_id], \
           results[dbh_id], \
           results[dhbh_id]


def main(docs_f, hashes_f, num_c, output_f, output_models):
    import os.path
    docs_folder = docs_f
    hashes_folder = hashes_f
    num_clusters = num_c
    output_file = output_f

    source_jsons, hash_jsons = app_get_json_inputs(docs_folder, hashes_folder)

    documents_by_strategies, documents_by_hashes, document_hashes_by_hashes = app_grouping_worker(source_jsons,
                                                                                                  hash_jsons)
    # todo models output should be configurable
    clustering_results = app_clustering_worker(num_clusters, output_models, documents_by_strategies,
                                               document_hashes_by_hashes)
    json_str = clustering_dict_to_json(clustering_results)
    input_output.write_and_close(output_file, json_str)
