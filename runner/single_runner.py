import argparse
from src import app

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-hf', "--hash_folder", help="where the hashes are located", )
parser.add_argument('-nc', "--num_clusters", help="how many clusters to use", )
parser.add_argument('-o', "--output", help="where the clustering result will be outputted", )

args = parser.parse_args()

if __name__ == '__main__':
    docs_folder = args.input_folder
    hashes_folder = args.hash_folder
    num_clusters = int(args.num_clusters)
    output_file = args.output

    app.main(docs_folder, hashes_folder, num_clusters, output_file)
    print("done!")
