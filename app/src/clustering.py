from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from app.src.models import ClusterContext
from sklearn.metrics import silhouette_score


def calculate_cluster_silhuette_score(matrix, model):
    labels = model.labels_
    return  silhouette_score(matrix, labels, metric='euclidean', sample_size=1500)

def create_cluster_context(num_clusters, id, documents):
    vectorizer = DictVectorizer()
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    X = vectorizer.fit_transform(dict_vectors)
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    silhuette = calculate_cluster_silhuette_score(X, model)
    return ClusterContext(id, model, vectorizer, silhuette)

def create_cluster_context_sink(num_clusters, id, documents, queue):
    cluster_context = create_cluster_context(num_clusters, id, documents)
    queue.put(cluster_context)
    return