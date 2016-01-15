import json
import os

with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
    configurationJSON = f.read()


class Config:
    parameters = json.loads(configurationJSON)
    def __init__(self):
        pass
