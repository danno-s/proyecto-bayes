import json
import os

with open(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/config.json', 'r') as f:
    text = f.read().split('/*')

configurationJSON = list()
for t in text:
    if '*/' not in t:
        configurationJSON = t


class Config:
    parameters = json.loads(configurationJSON)
    def __init__(self):
        pass
