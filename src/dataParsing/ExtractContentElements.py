#!/usr/bin/python

"""
Extrae URLs únicas de los eventos en la base de datos, y los árboles completos de URLs del sitio de las capturas
"""

import json
from src.utils.sqlUtils import sqlWrapper

def getMacroID(urls):
    """
    Obtiene el id en la base de datos de un árbol de urls

    Parameters
    ----------
    urls : string
        El árbol de urls a buscar
    Returns
    -------
    int
        El id del árbol de urls
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select id_n from urls where urls = '"+urls+"'"
    rows = sqlPD.read(sqlRead)
    return str(rows[0][0])

elements = ['TextAreas','InputText']

def getTextArea(d,L):
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


def extractContentElements():
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    sqlRead = 'SELECT DISTINCT urls,contentElements from pageview'
    rows = sqlGC.read(sqlRead)
    print(str(len(rows)) + " filas:")
    allElementsL = list()
    for i,row in enumerate(rows):
        data = dict()
        macro_id = getMacroID(str(row[0]))
        contentElementUnique = json.loads(row[1])
        for element in elements:
            try: data[element] = ' '.join(map(str, getStateVector(contentElementUnique,element)))
            except:
                print(json.dumps(contentElementUnique,indent=2))
                raise
        allElementsL.append((macro_id, data['TextAreas'],data['InputText']))

    macro_ids = set([x[0] for x in allElementsL])

    macroD = dict()
    for id in macro_ids:
        micro_states = set()
        for x in allElementsL:
            if x[0] == id:
                micro_states.add((x[1],x[2]))
        macroD[id]=micro_states

    for k,v in macroD.items():
        print("Macro ID "+str(k)+" : \n")
        [print("\t"+str(x)) for x in sorted(v)]
        print('\n')

    print("Total different elements:" + str(sum([len(x) for x in macroD.values()])))


    # Limpia las tablas

    sqlPD.truncate("contentElements")

    sqlWrite = "INSERT INTO contentElements (macro_id"
    for el in elements:
        sqlWrite = sqlWrite +','+el
    sqlWrite = sqlWrite+") VALUES (%s,%s,%s)"  # Guardar URLs desde evento.

    for id,values in macroD.items():
        for l in values:
            sqlPD.write(sqlWrite,(id,l[0],l[1]))

if __name__ == '__main__':
    extractContentElements()
