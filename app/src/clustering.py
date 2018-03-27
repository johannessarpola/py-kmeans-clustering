from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.feature_extraction import DictVectorizer
from app.src.models import ClusterContext
from sklearn.metrics import silhouette_score
from sklearn.externals import joblib


def create_kmeans_model(num_clusters, X):
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    return model


def create_minibatch_kmeans_model(num_clusters, X):
    model = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', batch_size=1000, n_init=1)
    model.fit(X)
    return model

def vectorize(documents):
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(dict_vectors)
    return (X,vectorizer)

def calculate_cluster_silhuette_score(X, model):
    labels = model.labels_
    return silhouette_score(X, labels, metric='euclidean', sample_size=1000)

def create_clustering_context(model, X, vectorizer, id):
    silhuette = calculate_cluster_silhuette_score(X, model)
    return ClusterContext(id, model, vectorizer, silhuette)

def create_cluster_context_sink(num_clusters, output_folder, id, documents, queue, minibatch = False):
    model = None
    X,vectorizer = vectorize(documents)
    if minibatch:
        model = create_minibatch_kmeans_model(num_clusters, X)
    else:
        model = create_kmeans_model(num_clusters, X)

    cluster_context = create_clustering_context(model, X, vectorizer, id)
    if(output_folder is not None):
        serialize_model(output_folder, id, cluster_context.cluster_model)
    queue.put(cluster_context)
    return


def serialize_model(folder, filename, model):
    path = f"{folder}/{filename}.model"
    joblib.dump(model, path)
    return path