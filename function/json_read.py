import json


def read_json(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data