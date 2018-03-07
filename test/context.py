import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import models
from app import adapter
from app import input_output
from app import aggregation

def relative_resource(path):
    dir = os.path.dirname(__file__)
    actual_path = os.path.join(dir, "resources", path)
    return actual_path

def path_to_resources():
    dir = os.path.dirname(__file__)
    folder_path = os.path.join(dir, "resources")
    return folder_path