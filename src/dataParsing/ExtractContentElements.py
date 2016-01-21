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

func = {'TextAreas':getTextAreas,'InputText':getInputText, 'RadioButton':getRadioButtons}
elementTypes= sorted([x for x in func.keys()])

def getStateVectorFrom(contentElements,type,L):
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
        getStateVectorFrom(child,type,L)

def getStateVector(contentElements,type):
    L = list()
    getStateVectorFrom(contentElements,type,L)
    return L









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
        data = dict()
        macro_id = getMacroID(str(row[0]))
        raw = row[1]
        contentElementUnique = json.loads(raw)
        for type in elementTypes:
            try: data[type] = ' '.join(map(str, getStateVector(contentElementUnique,type)))
            except:
                print(json.dumps(contentElementUnique,indent=2))
                raise
        allElementsL.append((macro_id, data['InputText'],data['RadioButton'],data['TextAreas'],raw))

    macro_ids = set([x[0] for x in allElementsL])

    macroD = dict()
    for id in macro_ids:
        micro_states = set()
        for x in allElementsL:
            if x[0] == id:
                micro_states.add((x[1],x[2],x[3],x[4]))
        macroD[id]=micro_states

    for id,values in macroD.items():
        print("MacroID "+str(id)+" :\n")
        for l in values:
            print("\t"+str((id,l[0],l[1],l[2])))

    print("Total different micro states:" + str(sum([len(x) for x in macroD.values()])))


    # Limpia las tablas

    sqlPD.truncate("contentElements")

    sqlWrite = "INSERT INTO contentElements (macro_id"
    for type in elementTypes:
        sqlWrite = sqlWrite +','+type
    sqlWrite = sqlWrite+",raw) VALUES (%s,%s"
    for type in elementTypes:
        sqlWrite = sqlWrite + ",%s"
    sqlWrite = sqlWrite+ ")"  # Guardar URLs desde evento.
    print(sqlWrite)
    for id,values in macroD.items():
        for l in values:
            print((id,l[0],l[1],l[2],l[3]))
            sqlPD.write(sqlWrite,(id,l[0],l[1],l[2],l[3]))

if __name__ == '__main__':
    extractContentElements()
