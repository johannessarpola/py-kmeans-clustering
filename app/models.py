class Document(object):
    id = ''
    max = 0
    min = 0
    strategy = ''
    vector = []

    def __init__(self, id, max, min, strategy, vector):
        self.id = id
        self.max = max
        self.min = min
        self.strategy = strategy
        self.vector = vector

    def vector_dict(self):
        dict = {}
        for v in self.vector:
            w,v = v.rsplit(':', 1)
            dict[w] = float(v)
        return dict

class DocumentHash(object):
    id = ''
    content = ''
    attributes = {}

    def __init__(self, id, content, attributes):
        self.id = id
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


class ClusterContext(object):
    id = ""
    cluster_model = {}
    vectorizer = {}

    def __init__(self, id, clustering_model, vectorizer):
        self.id = id
        self.cluster_model = clustering_model
        self.vectorizer = vectorizer
