from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN, AffinityPropagation, MeanShift, AgglomerativeClustering
import hdbscan
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer

from app.src import logger_factory
from app.src.models import ClusterContext
from sklearn.metrics import silhouette_score
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD
import _pickle as pickle

log_factory = logger_factory.LoggerFactory()
logger = log_factory.instance(__name__)

EUCLIDEAN_METRIC = 'euclidean'
COSINE_METRIC = 'cosine'

def create_kmeans_model(num_clusters, X, id=None):
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, EUCLIDEAN_METRIC, id)
    return model, model.predict, silhouette


def create_minibatch_kmeans_model(num_clusters, X, id=None):
    model = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', batch_size=1000, n_init=1)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, EUCLIDEAN_METRIC, id)
    return model, model.predict, silhouette


def train_classifier(X, model, metric=EUCLIDEAN_METRIC):
    logger.info('Starting to train KNeighborsClassifier')
    X_p = model.fit_predict(X)
    classifier = KNeighborsClassifier(n_neighbors=1, metric=metric).fit(X, X_p)
    return classifier


def create_dbscan_model(epsilon, X, min_samples=100, metric=COSINE_METRIC, id=None):
    model = DBSCAN(eps=epsilon, min_samples=min_samples, metric=metric)
    predictor = train_classifier(X, model)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    return model, predictor.predict, silhouette


def create_hdbscan_model(X, min_cluster_size=15, min_samples=5, metric=EUCLIDEAN_METRIC, id=None):
    model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric=metric)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    predictor = train_classifier(X, model)
    return model, predictor.predict, silhouette


def create_affinity_propagation_model(X, damping=0.5, max_iter=200, id=None):
    # Broken, gets stuck
    model = AffinityPropagation(damping=damping, max_iter=max_iter)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, id)
    return model, model.predict, silhouette


def create_mean_shift_propagation_model(X, metric=EUCLIDEAN_METRIC, cluster_all=False, bandwidth=0.175, id=None):
    # Broken gets stuck
    model = MeanShift(bandwidth=bandwidth, cluster_all=cluster_all, seeds=10)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    return model, model.predict, silhouette


# linkage for cosine only works for average
def create_agglomerative_model(X, num_clusters, id=None, metric=COSINE_METRIC, linkage='average'):
    # Broken gets stuck
    model = AgglomerativeClustering(n_clusters=num_clusters, affinity=metric, linkage=linkage)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    classifier = train_classifier(X, model, metric=metric)  # model has also fit_predict
    return model, classifier.predict, silhouette


def vectorize(documents, id=None):
    logger.info(f'{id}: Vectorizing')
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(dict_vectors)
    logger.info(f"{id}: Total number of features in raw vector space: {len(vectorizer.feature_names_)}")
    return X, vectorizer


def do_lsa(X, n_components=100, n_iter=10, random_state=None, id=None):
    logger.info('doing lsa')
    svd = TruncatedSVD(n_components=n_components, n_iter=n_iter, random_state=random_state)
    trunc_x = svd.fit_transform(X)
    logger.info(f"{id}: Total features after LSA: {n_components}")
    return trunc_x, svd


def calculate_cluster_silhuette_score(X, model, metric=EUCLIDEAN_METRIC, id=None):
    labels = model.labels_
    logger.info(f"{id}: {set(labels)} labels")
    return attempt_silhouette(X, labels, metric, sample_size_start=5000, max_attempts=3)


def attempt_silhouette(X, labels, metric=EUCLIDEAN_METRIC, sample_size_start=5000, max_attempts=3):
    attemps = 1
    while attemps <= max_attempts:
        try:
            return silhouette_score(X, labels, metric=metric, sample_size=5000 * attemps)
        except ValueError as e:
            attemps += 1
            logger.error(f"{id}: {attemps}/{max_attempts} Could not calculate silhouette value with error {e}")
    return 'NaN'


def calculate_original_silhouette(cluster_context: ClusterContext, documents, hashes, metric=EUCLIDEAN_METRIC):
    from numpy import ndarray, asanyarray
    vectorizer = DictVectorizer()
    logger.info(f"Calculating original silhouette score for {cluster_context.id}")
    doc_tuples = list(map(lambda d: (hashes[d.id][0].category(), d.vector_dict()), documents))
    doc_cats = asanyarray(list(map(lambda t: t[0], doc_tuples)))
    X = vectorizer.fit_transform(list(map(lambda t: t[1], doc_tuples)))
    return attempt_silhouette(X, asanyarray(doc_cats), metric=EUCLIDEAN_METRIC, sample_size_start=5000
                              , max_attempts=3)


def create_cluster_context_sink(num_clusters, output_folder, id, documents, queue, modeller='a', lsa=True):
    raw_X, vectorizer = vectorize(documents, id)
    lsa_X = None
    svd = None
    if lsa:
        lsa_X, svd = do_lsa(raw_X, n_components=100, n_iter=10, id=id)
    else:
        pass
    X = raw_X if lsa_X is None else lsa_X
    if modeller == 'minibatch':
        logger.info(f"minibatch model")
        model, predictionF, silhouette = create_minibatch_kmeans_model(num_clusters, X, id)
    elif modeller == 'affinity_propagation':
        logger.info(f"Creating affinity-propagation model")
        model, predictionF, silhouette = create_affinity_propagation_model(X, id)
    elif modeller == 'mean_shift':
        logger.info(f"Creating mean_shift")
        model, predictionF, silhouette = create_affinity_propagation_model(X, id)
    elif modeller == 'dbscan':
        logger.info(f"Creating dbscan model")
        model, predictionF, silhouette = create_dbscan_model(0.65, X, id)
    elif modeller == 'agglomerative':
        logger.info(f"Creating agglomerative model")
        model, predictionF, silhouette = create_agglomerative_model(X, num_clusters, id)
    elif modeller == 'hdbscan':
        logger.info(f"Creating hdbscan model")
        model, predictionF, silhouette = create_hdbscan_model(X, id)
    else:
        logger.info("Creating kmeans model")
        model, predictionF, silhouette = create_kmeans_model(num_clusters, X, id)
    logger.info(f"{id}: Done modelling")
    context = ClusterContext(id, model, vectorizer, silhouette, predictionF, svd)
    if output_folder is not None and model is not None:
        serialize_context(output_folder, id, context)
    queue.put(context)
    return


def serialize_context(folder, filename, context):
    path = f"{folder}/{filename}.ctx"
    with open(path, 'wb') as out:
        pickle.dump(context, out)
    return path


def purity_score(dict, total_size):
    all = []
    for cluster, cats in dict.items():
        max_in_clus = max(list(map(lambda t: t[1], cats.items())))
        all.append(max_in_clus)
    return sum(all) / total_size