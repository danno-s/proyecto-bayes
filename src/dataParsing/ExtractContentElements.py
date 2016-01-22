#!/usr/bin/python

"""
Extrae URLs únicas de los eventos en la base de datos, y los árboles completos de URLs del sitio de las capturas
"""

import json

from src.utils.dataParsingUtils import *


def getTextAreas(d,L):
    hasValue = d['HasValue']
    #isHidden = d['IsHidden']
    if True: #isHidden == 'false' or isHidden == 'true':
        if hasValue == 'true':
            L.append(1)
        else:
            L.append(0)


def getInputText(d,L):
    hasValue = d['HasValue']
    isHidden = d['IsHidden']
    if isHidden == 'false' or isHidden == 'true':
        if hasValue == 'true':
            L.append(1)
        else:
            L.append(0)

def getRadioButtons(d,L):
    selected = d['Selected']
    L.append(selected)

def getSelects(d,L):
    options = d['Selected']
    if len(options) >0:
        L.append('-'.join(options))

def getCheckboxes(d,L):
    quantity = int(d['Quantity'])
    vector = ['0']*quantity
    options = d['Selected']
    if options != '':
        for i in options:
            vector[int(i)]='1'
    L.append('-'.join(vector))
func = {'TextAreas':getTextAreas,'InputText':getInputText, 'RadioButton':getRadioButtons, 'Selects':getSelects,'Checkbox': getCheckboxes}
elementTypes= sorted([x for x in func.keys()])
print('elementTypes:' +str(elementTypes))

def generateStateVectorFrom(contentElements, type, L):
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
            func[type](el, L)
    children = contentElements['children']
    for child in children:
        generateStateVectorFrom(child, type, L)

def getStateVectors(contentElements,types):
    data = dict()
    for type in elementTypes:
        L = list()
        try:
            generateStateVectorFrom(contentElements, type, L)
            data[type] = ' '.join(map(str, L))
        except:
            print(json.dumps(contentElements,indent=2))
            raise
    return data

def extractContentElements():
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    sqlRead = 'SELECT DISTINCT urls,contentElements from pageview'
    rows = sqlGC.read(sqlRead)
    allElementsL = list()
    for i,row in enumerate(rows):
        eL = tuple()
        data = dict()
        macro_id = getMacroID(str(row[0]))
        raw = row[1]
        contentElementUnique = json.loads(raw)
        eL=eL+(macro_id,)
        try:
            data = getStateVectors(contentElementUnique,elementTypes)
        except:
            print(type + ", Fila: "+  str(i))
            print(json.dumps(contentElementUnique,indent=2))
            raise
        for type in elementTypes:
            eL = eL+(data[type],)
        eL = eL+(raw,)
        allElementsL.append(eL)

    macro_ids = set([x[0] for x in allElementsL])

    macroD = dict()
    for id in macro_ids:
        micro_states = set()
        for x in allElementsL:
            if x[0] == id:
                element_states = tuple()
                for st in x[1:]:
                    element_states += (st,)
                micro_states.add(element_states)
        macroD[id]=micro_states

    for id,values in macroD.items():
        print("MacroID "+str(id)+" :\n")
        for l in values:
            tp = (id,)
            for x in l[:-1]:
                tp += (x,)
            print("\t"+str(tp))

    print("Total different micro states:" + str(sum([len(x) for x in macroD.values()])))


    # Limpia las tablas

    sqlPD.truncate("contentElements")

    # Guarda sets únicos de elementos con sus macro_id en tabla contentElements.

    # Primero se guarda el marco_id y la estructura json raw
    sqlWrite = "INSERT INTO contentElements (macro_id,raw) VALUES (%s,%s)"
    print(sqlWrite)
    for id,values in macroD.items():
        for l in values:
            tp = (id,l[-1])
            sqlPD.write(sqlWrite,tp)
            # Luego se realiza un update sobre esta fila insertada
            # OBS: Se hizo así debido a que mysql.connector no soporta insertar más de 5 valores simultáneamente.
            sqlUpdate = "UPDATE contentElements SET "
            for type in elementTypes:
                sqlUpdate += type+'=%s,'
            tp = tuple()
            for x in l[:-1]:
                tp += (x,)
            sqlUpdate = sqlUpdate[:-1] + " ORDER BY id DESC LIMIT 1"
            sqlPD.write(sqlUpdate,tp)



if __name__ == '__main__':
    extractContentElements()
