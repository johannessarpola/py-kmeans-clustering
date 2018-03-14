import json
from os import path, walk


def get_jsons_from_folder(folder):
    files = get_filepaths_in_folder(folder)
    jsons = []
    for file in files:
        read_and_extend_collection_json_sink(file, jsons)
    return jsons


def get_filepaths_in_folder(folder):
    paths = []
    for dir, subdir, files in walk(folder):
        for file in files:
            p = path.join(dir, file)
            paths.append(p)
            print(p)
    return paths

def read_and_extend_collection_json_sink(file, collection):
    opened = open(file, "r")
    collection.append(json.load(opened))
    opened.close()

def write_and_close(path, content):
    out = open(path, 'w')
    out.write(content)
    out.close()