from app.src import adapter


def document_creator(json):
    return adapter.multiple_documents_from_json(json)


def document_hash_creator(json):
    return adapter.multiple_document_hashes_from_json(json)


def document_combiner(collection):
    return adapter.load_jsons_to_models(collection, document_creator)


def document_hash_combiner(collection):
    return adapter.load_jsons_to_models(collection, document_hash_creator)
