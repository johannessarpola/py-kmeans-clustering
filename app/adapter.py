import json
from . import models

def json_to_document(json):
    id = json["id"]
    max = json["max"]
    min = json["id"]
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