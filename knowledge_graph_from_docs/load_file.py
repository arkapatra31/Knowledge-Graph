import json
from dotenv import load_dotenv
import os


# Load the JSON file
def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

__all__ = [load_json_file]
