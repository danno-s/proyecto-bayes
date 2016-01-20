#!/usr/bin/python

"""
Extrae URLs únicas de los eventos en la base de datos, y los árboles completos de URLs del sitio de las capturas
"""

import json
from src.utils.sqlUtils import sqlWrapper

def getIDof(urls):
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
    sqlRead = 'select id_n from urls where urls = '+ "'"+urls+"'"
    rows = sqlPD.read(sqlRead)
    return str(rows[0][0])

elements = ['textAreas','inputText']

def getTextArea(d,L):
#    print("getTextArea("+str(d)+")")
    hasValue = d['hasValue']
    if hasValue == 'true':
        L.append(1)
    else:
        L.append(0)

def getInputText(d,L):
#    print("getInputText("+str(d)+")")
    hasValue = d['hasValue']
    isHidden = d['isHidden']
    if isHidden == 'false': # or isHidden == 'true':
        if hasValue == 'true':
            L.append(1)
        else:
            L.append(0)

def getStateVectorFromParent(parent,L,func):
    if parent == '':
        return
    elif isinstance(parent,list) and len(parent) > 0:
#        print("PARENT:"+str(len(parent)))
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

def getStateVectorFromChildren(d,L,func):
    if d == '':
        return
    parent = d['parent']
    getStateVectorFromParent(parent,L,func=func)
    children = d['children']
#    print("CHILDREN:"+str(len(children)))
    for child in children:
#        print("child"+str(child))
        getStateVectorFromParent(child,L,func=func)

def getStateVector(contentElements,type):
    L = list()
    rootD = dict()
    if type == 'textAreas':
        func = getTextArea
        rootD = contentElements['textareas']
    if type == 'inputText':
        func = getInputText
        rootD = contentElements['inputText']

    if len(rootD) > 0:
        parent = rootD['parent']
        getStateVectorFromParent(parent,L,func=func)
        children = rootD['children']
        for child in children:
            getStateVectorFromChildren(child,L,func=func)
    return L


def extractContentElementVectors():
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
   # sqlPD.truncate("contentElementsVectors")

    sqlRead = 'SELECT urls,contentElements from pageview'
    rows = sqlGC.read(sqlRead)
    assert len(rows)> 0
    for row in rows:
        contentElementsJSON= json.loads(row[1])
        vectors_data = dict()
        for element in elements:
            vectors_data[element] = ' '.join(map(str, getStateVector(contentElementsJSON,element)))
        urls_id = getIDof(row[0])
        sqlWrite = "INSERT INTO contentElementsVectors (macro_id, textAreas,inputText) VALUES (%s,%s)"  # Guardar URLs desde evento.
        print((urls_id, vectors_data['textAreas'],vectors_data['inputText']))
        #sqlPD.write(sqlWrite,(urls_id, vectors_data['textAreas'],vectors_data['inputText']))


if __name__ == '__main__':
    extractContentElementVectors()
