import argparse
from app.src import app
import os

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-hf', "--hash_folder", help="where the hashes are located", )
parser.add_argument('-nc', "--num_clusters", help="how many clusters to use", )
parser.add_argument('-o', "--output", help="where the clustering result will be outputted", )
parser.add_argument('-om', "--output-models", help="where the cluster models will be outputted", )

args = parser.parse_args()

if __name__ == '__main__':
    docs_folder = args.input_folder
    hashes_folder = args.hash_folder
    num_clusters = int(args.num_clusters)
    output_file = args.output
    output_models = args.output_models

    if output_models is None:
        output_models = os.path.dirname(output_file)

    if not os.path.exists(output_models):
        os.makedirs(output_models)

    app.main(docs_folder, hashes_folder, num_clusters, output_file, output_models)
    print("done!")
