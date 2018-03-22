class Identified(object):
    id = ''

    def __init__(self, id):
        self.id = id

    def asDict(self):
        d = {}
        d['id'] = self.id
        return d


class Document(Identified):
    max = 0
    min = 0
    strategy = ''
    vector = []

    def __init__(self, id, max, min, strategy, vector):
        super().__init__(id)
        self.max = max
        self.min = min
        self.strategy = strategy
        self.vector = vector

    def vector_dict(self):
        dict = {}
        for v in self.vector:
            w, v = v.rsplit(':', 1)
            dict[w] = float(v)
        return dict


class DocumentHash(Identified):
    content = ''
    attributes = {}

    def __init__(self, id, content, attributes):
        super().__init__(id)
        self.content = content
        self.attributes = attributes

    def category(self):
        if 'category' in self.attributes:
            return self.attributes['category']
        else:
            print('category was not in attributes')
            return ""

    def original(self):
        if 'original' in self.attributes:
            return self.attributes['original']
        else:
            print('original was not in attributes')
            return ''


class ClusterContext(Identified):
    cluster_model = {}
    vectorizer = {}
    silhuette_coefficent = 0.0

    def __init__(self, id, clustering_model,
                 vectorizer, silhuette):
        super().__init__(id)
        self.cluster_model = clustering_model
        self.vectorizer = vectorizer
        self.silhuette_coefficent = silhuette


class CountElement(Identified):
    cnt = 0

    def __init__(self, id, cnt):
        super().__init__(id)
        self.cnt = cnt


class DictElement(Identified):
    data_key = ''
    data = {}

    def __init__(self, id, data, data_key='data'):
        super().__init__(id)
        self.data_key = data_key
        self.data = data

    def asJson(self):
        base = super().asDict()
        base[self.data_key] = self.data
        return base


class ClusteringResult(DictElement):
    silhouette = 0.0
    path_to_model = ""
    def __init__(self, id, clusters, silhouette, path_to_model=""):
        super().__init__(id, clusters, 'clusters')
        self.silhouette = silhouette
        self.path_to_model = path_to_model

    def asJson(self):
        base = super().asJson()
        base['silhouette'] = self.silhouette
        base['path_to_model'] = self.path_to_model
        return base


class Cluster(DictElement):
    def __init__(self, id, clusters):
        super().__init__(id, clusters, 'categories')

