import argparse
import json
import multiprocessing as mp
from collections import defaultdict, OrderedDict

import model_utils
import multiprocessing_utils as mpu
from app import aggregation, input_output

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-hf', "--hash_folder", help="where the hashes are located", )
parser.add_argument('-nc', "--num_clusters", help="how many clusters to use", )
parser.add_argument('-o', "--output", help="where the clustering result will be outputted", )

args = parser.parse_args()

docs_folder = args.input_folder
hashes_folder = args.hash_folder
num_clusters = int(args.num_clusters)
output_file = args.output


def app_get_json_inputs(docs_folder, hashes_folder):
    source_jsons = input_output.get_jsons_from_folder(docs_folder)
    hash_jsons = input_output.get_jsons_from_folder(hashes_folder)
    return (source_jsons, hash_jsons)


def app_create_categories_from_clustering(cluster_context,
                                          documents,
                                          document_hashes_by_hashes,
                                          queue):
    categories = defaultdict(dict)
    cluster_model = cluster_context.cluster_model
    vectorizer = cluster_context.vectorizer

    for document in documents:
        document_vector = vectorizer.transform(document.vector_dict())
        # Prediction is cluster id which is from [0] ... [n]
        prediction = cluster_model.predict(document_vector)
        category = document_hashes_by_hashes[document.id][0].category()
        if category in categories[str(prediction)]:
            # Increment occurence by one
            categories[str(prediction)][category] = categories[str(prediction)][category] + 1
        else:
            # If not exist initialize with 1
            categories[str(prediction)][category] = 1
    # Sort by categories which are from 0 .. n
    sorted_dict = OrderedDict(sorted(categories.items(), key=lambda t: t[0]))
    # Put (id, dict) to queue
    queue.put((cluster_context.id, sorted_dict))


def app_do_clustering(documents_by_strategies, document_hashes_by_hashes, cluster_contexts, queue):
    processes = []
    for cluster_context in cluster_contexts:
        documents = documents_by_strategies[cluster_context.id]
        p = mpu.create_process_and_start(app_create_categories_from_clustering,
                                         (cluster_context, documents, document_hashes_by_hashes, queue),
                                         f"Started {cluster_context.id} clustering")
        processes.append(p)
    return processes


def app_create_cluster_context(num_clusters, documents_by_strategies, queue):
    """"""
    from clustering import create_cluster_context_sink
    processes = []
    for (strategy, documents) in documents_by_strategies.items():
        p = mpu.create_process_and_start(create_cluster_context_sink,
                                         (num_clusters, strategy, documents, queue),
                                         f"Started {strategy} cluster context modelling")
        processes.append(p)
    return processes


def app_create_cluster_context_worker(num_clusters, documents_by_strategies):
    queue = mp.Queue()
    processes = app_create_cluster_context(num_clusters, documents_by_strategies, queue)
    cluster_context = mpu.gather_to_list_and_join(queue, processes)
    queue.close()
    return cluster_context


def app_do_clustering_worker(documents_by_strategies, document_hashes_by_hashes, cluster_context):
    queue = mp.Queue()
    processes = app_do_clustering(documents_by_strategies, document_hashes_by_hashes, cluster_context, queue)
    categories_by_clusters = mpu.gather_to_dict_from_tuples_and_join(queue, processes)
    queue.close()
    return categories_by_clusters


def app_gather_result(documents_by_strategies, document_hashes_by_hashes):
    cluster_context = app_create_cluster_context_worker(num_clusters, documents_by_strategies)
    categories_by_clusters = app_do_clustering_worker(documents_by_strategies, document_hashes_by_hashes,
                                                      cluster_context)
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
                                         (dbs_id, 'strategy', model_utils.document_combiner,
                                          source_jsons, queue),
                                         f"Started grouping with id: {dbs_id}")

    p_dbh = mpu.create_process_and_start(do_grouping_sink,
                                         (dbh_id, 'id', model_utils.document_combiner,
                                          source_jsons, queue),
                                         f"Started grouping with id: {dbh_id}")

    p_dhbh = mpu.create_process_and_start(do_grouping_sink,
                                          (dhbh_id, 'id', model_utils.document_hash_combiner,
                                           hash_jsons, queue),
                                          f"Started grouping with id: {dhbh_id}")

    results = mpu.gather_to_dict_from_tuples_and_join(queue, [p_dbs, p_dbh, p_dhbh])
    queue.close()
    return results[dbs_id], \
           results[dbh_id], \
           results[dhbh_id]


if __name__ == '__main__':
    source_jsons, hash_jsons = app_get_json_inputs(docs_folder, hashes_folder)

    documents_by_strategies, documents_by_hashes, document_hashes_by_hashes = app_grouping_worker(source_jsons,
                                                                                                  hash_jsons)
    clustering_results = app_gather_result(documents_by_strategies, document_hashes_by_hashes)

    result_json = json.dumps(clustering_results, indent=4)
    input_output.write_and_close(output_file, result_json)

    print("done!")
