import json
import argparse
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction import DictVectorizer
from app import adapter, locator, aggregation, input
from os import listdir, walk, path
from os.path import isfile, join

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-hf', "--hash_folder", help="where the hashes are located", )

args = parser.parse_args()

docs_folder = args.input_folder  # locator.relative_resource(args.input_folder)
hashes_folder = args.hash_folder  # locator.relative_resource(args.hash_folder)


def app_get_json_inputs(docs_folder, hashes_folder):
    source_jsons = input.get_jsons_from_folder(docs_folder)
    hash_jsons = input.get_jsons_from_folder(hashes_folder)
    return (source_jsons, hash_jsons)


# List of all document jsons

source_jsons, hash_jsons = app_get_json_inputs(docs_folder, hashes_folder)

document_creator = lambda e: adapter.multiple_documents_from_json(e)
document_hash_creator = lambda e: adapter.multiple_document_hashes_from_json(e)

all_document_models_combiner = lambda collection: adapter.load_jsons_to_models(collection, document_creator)
all_document_hashes_models_combiner = lambda collection: adapter.load_jsons_to_models(collection, document_hash_creator)

documents_by_strategies = aggregation.group_by_attribute(all_document_models_combiner(source_jsons), 'strategy')
document_hashes_by_hashes = aggregation.group_by_attribute(all_document_hashes_models_combiner(hash_jsons), 'id')

print("done")
