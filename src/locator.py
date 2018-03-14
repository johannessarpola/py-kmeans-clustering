import os

def relative_resource(path):
    dir = os.path.dirname(__file__)
    res = os.path.join(dir, "resources")
    actual_path = os.path.join(res, path)
    return actual_path