#!/usr/bin/python

import json
from src.simulated.utils.loadConfig import Config


class MicroStateVectorExtractor():

    def __init__(self):
        __allFuncs = {
            'TextAreas':    self.__getTextAreas,
            'InputText':    self.__getInputText,
            'RadioButton':  self.__getRadioButtons,
            'Selects':      self.__getSelects,
            'Checkbox':     self.__getCheckboxes
            }
        self.elementTypes= sorted(Config().getArray(attr='elementTypes'))
        self.availableTypes = ' / '.join([x for x in sorted(__allFuncs.keys())])
        #self.elementTypes = [x for x in sorted(__allFuncs.keys()) if x in types]
        self.funcD = dict()
        for type in self.elementTypes:
            try:
                self.funcD[type]=__allFuncs[type]
            except KeyError:
                print("Type '"+type+"' is not a valid element type for the extractor.")
                print("Please check that your types array in Config.json contains only these:\n"+str(self.getAvailableTypes()))

    def getElementTypes(self):
        return sorted(self.elementTypes)

    def getAvailableTypes(self):
        return self.availableTypes

    def __getTextAreas(self,d,L):
        hasValue = d['HasValue']
        #isHidden = d['IsHidden']
        if True: #isHidden == 'false' or isHidden == 'true':
            if hasValue == 'true':
                L.append(1)
            else:
                L.append(0)

    def __getInputText(self,d,L):
        hasValue = d['HasValue']
        isHidden = d['IsHidden']
        if isHidden == 'false' or isHidden == 'true':
            if hasValue == 'true':
                L.append(1)
            else:
                L.append(0)

    def __getRadioButtons(self,d,L):
        selected = d['Selected']
        L.append(selected)

    def __getSelects(self,d,L):
        options = d['Selected']
        if len(options) >0:
            L.append('-'.join(options))

    def __getCheckboxes(self,d,L):
        quantity = int(d['Quantity'])
        vector = ['0']*quantity
        options = d['Selected']
        if options != '':
            for i in options:
                vector[int(i)]='1'
        L.append('-'.join(vector))

    def generateStateVectorFrom(self,contentElements, type, L):
        if len(contentElements) == 0:
            return
        valueD = contentElements['value']
        try:
            elementL = valueD[type]
        except:
            print(valueD)
            raise
        if elementL != '':
            for el in elementL:
                self.funcD[type](el, L)
        children = contentElements['children']
        for child in children:
            self.generateStateVectorFrom(child, type, L)

    def getStateVectors(self,contentElements):
        data = dict()
        for type in self.elementTypes:
            L = list()
            try:
                self.generateStateVectorFrom(contentElements, type, L)
                data[type] = ' '.join(map(str, L))
            except:
                print(json.dumps(contentElements,indent=2))
                raise
        return data