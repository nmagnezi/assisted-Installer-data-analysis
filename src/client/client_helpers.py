import json
import subprocess
import os


def build_search_index_by_id(obj_list):
    return {obj["id"]: obj for obj in obj_list}


def load_json_from_file(file):
    with open(file, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object


def get_token():
    token = os.getenv('TOKEN')
    if token:
        return token
    return subprocess.check_output('ocm token', shell=True).decode("utf-8")[:-1]
