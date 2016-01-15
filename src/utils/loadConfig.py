import json
import os

with open(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/config.json', 'r') as f:
    configurationJSON = f.read()

parameters = json.loads(configurationJSON)
print(parameters)

class Config:
    def __init__(self):
        pass
