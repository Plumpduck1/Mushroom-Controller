import json

CONFIG_FILE = "config.json"


def load_config():

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def save_config(data):

    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)