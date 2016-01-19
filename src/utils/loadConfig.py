import json
import os
import jsmin

with open(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/config.json', 'r') as f:
    configurationJSON = jsmin.jsmin(f.read())


class Config:
    __parameters = json.loads(configurationJSON)

    def __init__(self):
        pass

    def getValue(self,attr,mode):
        if mode == 'INT':
            return int(self.__parameters[attr])
        return self.__parameters[attr]

