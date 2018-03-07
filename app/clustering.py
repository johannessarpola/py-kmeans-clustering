from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from models import ClusterContext




def create_cluster_context(num_clusters, id, documents):
    vectorizer = DictVectorizer()
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    X = vectorizer.fit_transform(dict_vectors)
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    return ClusterContext(id, model, vectorizer)

def create_cluster_context_sink(num_clusters, id, documents, queue):
    result = create_cluster_context(num_clusters, id, documents)
    queue.put(result)
    return