import json
from app.src import models
from app.src.obj_utils import call_if_obj_has_method_or_default


def json_to_document(json):
    id = json["id"]
    max = json["max"]
    min = json["min"]
    strategy = json["strategy"]
    vector = json["vector"]
    return models.Document(id, max, min, strategy, vector)


def json_to_document_hash(json):
    id = json["hash"]
    content = json["content"]
    attributes = json["attributes"]
    return models.DocumentHash(id, content, attributes)


def documents_from_strings(lst):
    docs = []
    for s in lst:
        j = json.loads(s)
        docs.append(json_to_document(j))


def document_hashes_from_strings(lst):
    docs = []
    for s in lst:
        j = json.loads(s)
        docs.append(json_to_document_hash(j))


def multiple_documents_from_json(json):
    docs = []
    for obj in json:
        docs.append(json_to_document(obj))
    return docs


def multiple_document_hashes_from_json(json):
    docs = []
    for obj in json:
        docs.append(json_to_document_hash(obj))
    return docs


def load_jsons_to_models(jsons, creator):
    all_models = []
    for json in jsons:
        models = creator(json)
        all_models.extend(models)
    return all_models


def toJsonFormat(obj):
    jsonObj = call_if_obj_has_method_or_default(obj, 'asJson', obj)
    return jsonObj

def cluster_dict_to_output_format(dict):
    result = []
    # v is tuple of context and clustering results in dict
    for (k, v) in dict.items():
        des = []
        clusters,context = v
        for (i,c) in clusters.items():
            des.append(models.Cluster(i, c).asJson())
        result.append(models.ClusteringResult(k, des, context.silhuette_coefficent).asJson())
    return result


def clustering_dict_to_json(dict):
    r = cluster_dict_to_output_format(dict)
    return json.dumps(r, indent=4, default=lambda o: o.__dict__)