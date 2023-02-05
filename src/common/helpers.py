import json
import logging


def configure_logger(debug_mode):
    logging.basicConfig(
        level=logging.DEBUG if debug_mode is True else logging.INFO,
        format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
    )


def load_json_from_file(file):
    with open(file, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object
