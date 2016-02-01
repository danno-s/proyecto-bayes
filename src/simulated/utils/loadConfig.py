import json
import os
import jsmin

with open(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/config.json', 'r') as f:
    configurationJSON = jsmin.jsmin(f.read())


class Config:
    __parameters = json.loads(configurationJSON)

    def __init__(self):
        pass

    def getValue(self, attr, mode=None):
        if mode is not None:
            if mode == 'INT':
                value = int(self.__parameters[attr])
                assert value > 0
            return value
        return self.__parameters[attr]

    def getArray(self,attr):
        jsonArray = self.__parameters[attr]
        assert len(jsonArray)>0
        return jsonArray