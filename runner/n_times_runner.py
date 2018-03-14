
import argparse
import gc
from app.src import app

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-hf', "--hash_folder", help="where the hashes are located", )
parser.add_argument('-nc', "--num_clusters", help="how many clusters to use", )
parser.add_argument('-o', "--output", help="where the clustering result will be outputted", )
parser.add_argument('-n', "--ntimes", help="how many times clustering is run", )

args = parser.parse_args()

if __name__ == '__main__':
    docs_folder = args.input_folder
    hashes_folder = args.hash_folder
    num_clusters = int(args.num_clusters)
    output_file = args.output
    for i in range(0, int(args.ntimes)):
        (f, e) = output_file.rsplit('.', 1)
        app.main(docs_folder, hashes_folder, num_clusters, f"{f}_{i}.{e}")
        gc.collect()
    print("done!")
