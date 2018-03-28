from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
import hdbscan
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer
from app.src.models import ClusterContext
from sklearn.metrics import silhouette_score
from sklearn.externals import joblib


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


def create_dbscan_model(epsilon, X, min_samples=10):
    model = DBSCAN(eps=epsilon, min_samples=min_samples, metric='cosine')
    x_p = model.fit_predict(X)
    predictor = KNeighborsClassifier().fit(X, x_p)
    silhouette = calculate_cluster_silhuette_score(X, model, 'cosine')
    return model, predictor.predict, silhouette


def create_hdbscan_model(epsilon, X, min_samples=5):
    model = hdbscan.HDBSCAN(min_cluster_size=min_samples, metric='cosine')
    x_p = model.fit_predict(X)
    predictor = KNeighborsClassifier().fit(X, x_p)
    silhouette = calculate_cluster_silhuette_score(X, model, 'cosine')
    return model, predictor.predict, silhouette


def vectorize(documents):
    dict_vectors = list(map(lambda d: d.vector_dict(), documents))
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(dict_vectors)
    return (X, vectorizer)


def calculate_cluster_silhuette_score(X, model, metric='euclidean'):
    labels = model.labels_
    print(set(labels))
    return silhouette_score(X, labels, metric=metric, sample_size=1000)


def create_cluster_context_sink(num_clusters, output_folder, id, documents, queue, modeller='hdbscan'):
    X, vectorizer = vectorize(documents)
    if modeller == 'minibatch':
        print(f"minibatch model")
        model, predictionF, silhouette = create_minibatch_kmeans_model(num_clusters, X)
    elif modeller == 'dbscan':
        print(f"dbscan model")
        model, predictionF, silhouette = create_dbscan_model(0.65, X)  # TODO Test with couple epsilons
    elif modeller == 'hdbscan':
        print(f"hdbscan")
        model, predictionF, silhouette = create_hdbscan_model(0, X)
    else:
        print("kmeans model")
        model, predictionF, silhouette = create_kmeans_model(num_clusters, X)
    context = ClusterContext(id, model, vectorizer, silhouette, X, predictionF)
    if (output_folder is not None):
        serialize_model(output_folder, id, context.cluster_model)
    queue.put(context)
    return


def serialize_model(folder, filename, model):
    path = f"{folder}/{filename}.model"
    joblib.dump(model, path)
    return path
