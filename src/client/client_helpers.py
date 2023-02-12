import json


def build_search_index_by_id(obj_list):
    return {obj["id"]: obj for obj in obj_list}


def load_json_from_file(file):
    with open(file, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object
