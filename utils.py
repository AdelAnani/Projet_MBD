import json


def load_json(path):
    with open(path, "r") as lst:
        alb = json.load(lst)

    return alb
