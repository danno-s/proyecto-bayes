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

elementTypes = ['TextAreas', 'InputText']
func = {'TextAreas':getTextAreas,'InputText':getInputText}

'''

def getStateVectorFromParent(parent,L,func):
    if parent == '':
        return
    elif isinstance(parent,list) and len(parent) > 0:
        for p in parent:
            if isinstance(p,dict):
                func(p,L)
    else:
        p = parent['parent']
        getStateVectorFromParent(p,L,func = func)
        children = parent['children']
        if isinstance(children,list) and len(children) > 0:
            for ch in children:
                getStateVectorFromChildren(ch,L,func=func)
            return


def getStateVectorFromChildren(p,L,func):
    if p == '':
        return
    parent = p['parent']
    getStateVectorFromParent(parent,L,func=func)
    children = p['children']
    for child in children:
        getStateVectorFromParent(child,L,func=func)


def getStateVector(contentElements,type):
    L = list()
    rootD = dict()
    if type in elements:
        func = getTextArea
        try:
            rootD = contentElements[type]
        except:
            raise
    if len(rootD) > 0:
        parent = rootD['parent']
        getStateVectorFromParent(parent,L,func=func)
        children = rootD['children']
        for child in children:
            getStateVectorFromChildren(child,L,func=func)
    return L
'''
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
                #print(json.dumps(contentElementUnique,indent=2))
                raise
        allElementsL.append((macro_id, data['TextAreas'],data['InputText'],raw))

    macro_ids = set([x[0] for x in allElementsL])

    macroD = dict()
    for id in macro_ids:
        micro_states = set()
        for x in allElementsL:
            if x[0] == id:
                micro_states.add((x[1],x[2],x[3]))
        macroD[id]=micro_states

   # for k,v in macroD.items():
   #     print("Macro ID "+str(k)+" : \n")
   #     [print("\t" + str(x) for x in sorted([(a[2], a[3]) for a in v]))]
   #     print('\n')

    print("Total different micro states:" + str(sum([len(x) for x in macroD.values()])))

'''
    # Limpia las tablas

    sqlPD.truncate("contentElements")

    sqlWrite = "INSERT INTO contentElements (macro_id"
    for el in elements:
        sqlWrite = sqlWrite +','+el
    sqlWrite = sqlWrite+",raw) VALUES (%s,%s,%s,%s)"  # Guardar URLs desde evento.

    for id,values in macroD.items():
        for l in values:
            sqlPD.write(sqlWrite,(id,l[0],l[1],l[2]))
'''
if __name__ == '__main__':
    extractContentElements()
