from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN, AffinityPropagation, MeanShift
import hdbscan
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer
from app.src.models import ClusterContext
from sklearn.metrics import silhouette_score
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD


def create_kmeans_model(num_clusters, X):
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, 'euclidean')
    return model, model.predict, silhouette


def create_minibatch_kmeans_model(num_clusters, X):
    model = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', batch_size=1000, n_init=1)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, 'euclidean')
    return model, model.predict, silhouette


def create_dbscan_model(epsilon, X, min_samples=100, metric='cosine'):
    model = DBSCAN(eps=epsilon, min_samples=min_samples, metric=metric)
    x_p = model.fit_predict(X)
    print('starting KNeighborsClassifier')
    predictor = KNeighborsClassifier().fit(X, x_p)
    silhouette = calculate_cluster_silhuette_score(X, model, metric)
    return model, predictor.predict, silhouette


def create_hdbscan_model(X, min_cluster_size=15, min_samples=5, metric='euclidean'):
    model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric=metric)
    x_p = model.fit_predict(X)
    silhouette = calculate_cluster_silhuette_score(X, model, metric)
    print('starting KNeighborsClassifier')
    predictor = KNeighborsClassifier().fit(X, x_p)
    return model, predictor.predict, silhouette


def create_affinity_propagation_model(X, damping=0.5, max_iter=200):
    # Broken, gets stuck
    model = AffinityPropagation(damping=damping, max_iter=max_iter)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model)
    return model, model.predict, silhouette


def create_mean_shift_propagation(X, metric='euclidean', cluster_all= False, bandwidth=0.175):
    # Broken gets stuck
    model = MeanShift(bandwidth=bandwidth, cluster_all=cluster_all, seeds=10)
    model.fit(X)
    silhouette = calculate_cluster_silhuette_score(X, model, metric)
    return model, model.predict, silhouette


def vectorize(documents):
    print('vectorizing')
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(dict_vectors)
    print(f"total features: {len(vectorizer.feature_names_)}")
    return X, vectorizer


def do_lsa(X, n_components=100, n_iter=10, random_state=None):
    print('doing lsa')
    svd = TruncatedSVD(n_components=n_components, n_iter=n_iter, random_state=random_state)
    trunc_x = svd.fit_transform(X)
    print(f"total features: {n_components}")
    return trunc_x, svd


def calculate_cluster_silhuette_score(X, model, metric='euclidean'):
    labels = model.labels_
    print(set(labels))
    return silhouette_score(X, labels, metric=metric, sample_size=1000)


def create_cluster_context_sink(num_clusters, output_folder, id, documents, queue, modeller='kmeans', lsa=True):
    raw_X, vectorizer = vectorize(documents)
    lsa_X = None
    svd = None
    if lsa:
        lsa_X, svd = do_lsa(raw_X, n_components=100, n_iter=10)
    else:
        pass
    X = raw_X if lsa_X is None else lsa_X
    if modeller == 'minibatch':
        print(f"minibatch model")
        model, predictionF, silhouette = create_minibatch_kmeans_model(num_clusters, X)
    elif modeller == 'affinity_propagation':
        print(f"affinity-propagation model")
        model, predictionF, silhouette = create_affinity_propagation_model(X)
    elif modeller == 'mean_shift':
        print(f"mean_shift")
        model, predictionF, silhouette = create_affinity_propagation_model(X)
    elif modeller == 'dbscan':
        print(f"dbscan model")
        model, predictionF, silhouette = create_dbscan_model(0.65, X)
    elif modeller == 'hdbscan':
        print(f"hdbscan")
        model, predictionF, silhouette = create_hdbscan_model(X)
    else:
        print("kmeans model")
        model, predictionF, silhouette = create_kmeans_model(num_clusters, X)
    print('done modelling')
    context = ClusterContext(id, model, vectorizer, silhouette, X, predictionF, svd)
    if output_folder is not None and model is not None:
        serialize_model(output_folder, id, model)
    queue.put(context)
    return


def serialize_model(folder, filename, model):
    path = f"{folder}/{filename}.model"
    joblib.dump(model, path)
    return path
