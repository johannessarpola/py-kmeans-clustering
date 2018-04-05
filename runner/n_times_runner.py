
import argparse
import gc
import os

from app.src import app

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-hf', "--hash_folder", help="where the hashes are located", )
parser.add_argument('-nc', "--num_clusters", help="how many clusters to use", )
parser.add_argument('-o', "--output", help="where the clustering result will be outputted", )
parser.add_argument('-n', "--ntimes", help="how many times clustering is run", )
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

    for i in range(0, int(args.ntimes)):
        print(f"-- Running {i}/{args.ntimes}")
        (f, e) = output_file.rsplit('.', 1)
        models_path =  f"{output_models}/{i}"
        if not os.path.exists(models_path):
            os.makedirs(models_path)
        app.main(docs_folder, hashes_folder, num_clusters, f"{f}_{i}.{e}", models_path)
        gc.collect()
        print(f"-- Done with {i + 1}/{args.ntimes} iteration")
    print("-- Runner is finished!")
    import sys
    sys.exit(0)
