from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN, AffinityPropagation, MeanShift
import hdbscan
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer

from app.src import logger_factory
from app.src.models import ClusterContext
from sklearn.metrics import silhouette_score
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD

log_factory = logger_factory.LoggerFactory()
logger = log_factory.instance(__name__)


def create_kmeans_model(num_clusters, X, id = None):
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, 'euclidean', id)
    return model, model.predict, silhouette


def create_minibatch_kmeans_model(num_clusters, X, id = None):
    model = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', batch_size=1000, n_init=1)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, 'euclidean', id)
    return model, model.predict, silhouette


def train_classifier(X, model):
    logger.info('Starting to train KNeighborsClassifier')
    X_p = model.fit_predict(X)
    classifier = KNeighborsClassifier().fit(X, X_p)
    return classifier

def create_dbscan_model(epsilon, X, min_samples=100, metric='cosine', id = None):
    model = DBSCAN(eps=epsilon, min_samples=min_samples, metric=metric)
    predictor = train_classifier(X, model)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    return model, predictor.predict, silhouette


def create_hdbscan_model(X, min_cluster_size=15, min_samples=5, metric='euclidean', id = None):
    model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric=metric)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    predictor = train_classifier(X, model)
    return model, predictor.predict, silhouette


def create_affinity_propagation_model(X, damping=0.5, max_iter=200, id = None):
    # Broken, gets stuck
    model = AffinityPropagation(damping=damping, max_iter=max_iter)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, id)
    return model, model.predict, silhouette


def create_mean_shift_propagation(X, metric='euclidean', cluster_all= False, bandwidth=0.175, id = None):
    # Broken gets stuck
    model = MeanShift(bandwidth=bandwidth, cluster_all=cluster_all, seeds=10)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, metric, id)
    return model, model.predict, silhouette


def vectorize(documents, id = None):
    logger.info('vectorizing')
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(dict_vectors)
    logger.info(f"{id}: Total number of features in raw vector space: {len(vectorizer.feature_names_)}")
    return X, vectorizer


def do_lsa(X, n_components=100, n_iter=10, random_state=None, id = None):
    logger.info('doing lsa')
    svd = TruncatedSVD(n_components=n_components, n_iter=n_iter, random_state=random_state)
    trunc_x = svd.fit_transform(X)
    logger.info(f"{id}: Total features after LSA: {n_components}")
    return trunc_x, svd


def calculate_cluster_silhuette_score(X, model, metric='euclidean', id = None):
    labels = model.labels_
    logger.info(f"{id}: {set(labels)} labels")
    attemps = 1
    max_attempts = 10
    while attemps <= max_attempts:
        try:
            return silhouette_score(X, labels, metric=metric, sample_size=1000 * attemps)
        except ValueError as e:
            attemps += 1
            logger.error(f"{id}: {attemps}/{max_attempts} Could not calculate silhouette value with error {e}")
    return 'NaN'


def create_cluster_context_sink(num_clusters, output_folder, id, documents, queue, modeller='kmeans', lsa=True):
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
    elif modeller == 'hdbscan':
        logger.info(f"Creating hdbscan model")
        model, predictionF, silhouette = create_hdbscan_model(X, id)
    else:
        logger.info("Creating kmeans model")
        model, predictionF, silhouette = create_kmeans_model(num_clusters, X, id)
    logger.info(f"{id}: Done modelling")
    context = ClusterContext(id, model, vectorizer, silhouette, X, predictionF, svd)
    if output_folder is not None and model is not None:
        serialize_model(output_folder, id, model)
    queue.put(context)
    return


def serialize_model(folder, filename, model):
    path = f"{folder}/{filename}.model"
    joblib.dump(model, path)
    return path
