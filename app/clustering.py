from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from models import ClusteringResult




def create_clustering(num_clusters, id, documents):
    vectorizer = DictVectorizer()
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    X = vectorizer.fit_transform(dict_vectors)
    model = KMeans(n_clusters=num_clusters, init='k-means++')
    model.fit(X)
    return ClusteringResult(id, model, vectorizer)

def create_clustering_sink(num_clusters, id, documents, queue):
    result = create_clustering(num_clusters, id, documents)
    queue.put(result)
    return