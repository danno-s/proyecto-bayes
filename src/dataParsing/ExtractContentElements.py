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
    sqlRead = "select id_n from urls where urls = '"+urls+"'"
    rows = sqlPD.read(sqlRead)
    print(rows)
    return str(rows[0][0])

elements = ['TextAreas','InputText']

def getTextArea(d,L):
#    print("getTextArea("+str(d)+")")
    hasValue = d['HasValue']
    if hasValue == 'true':
        L.append(1)
    else:
        L.append(0)

def getInputText(d,L):
#    print("getInputText("+str(d)+")")
    hasValue = d['HasValue']
    isHidden = d['IsHidden']
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
        try: p = parent['parent']
        except:
            print(func.__name__)
            raise
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
        print("FILA i= "+str(i) + str(row[0]))
        macro_id = getIDof(str(row[0]))
        contentElementUnique = json.loads(row[1])
        for element in elements:
            try: data[element] = ' '.join(map(str, getStateVector(contentElementUnique,element)))
            except:
                print(json.dumps(contentElementUnique,indent=2))
                raise
        allElementsL.append((macro_id, data['TextAreas'],data['InputText']))

    macro_ids = sorted(set([x[0] for x in allElementsL]))

    macroD = dict()
    for id in macro_ids:
        macroD[id]=[(x[1],x[2]) for x in allElementsL if x[0] == id]

    for k,v in sorted(macroD.items()):
        print(str(k)+" : \n")
        [print(str(x)) for x in v]
        print('\n')

    print("Total different elements:" + str(len(allElementsL)))
    for v in allElementsL:
        print(v)

''''

    # Limpia las tablas
    sqlPD.truncate("url")
    sqlPD.truncate("urls")


    sqlWrite = "INSERT INTO url (url) VALUES ("  # Guardar URLs desde evento.

    for url in L:
        sqlPD.write(sqlWrite + '"' + url + '");')

    sqlWrite = "INSERT INTO urls (id, urls) VALUES (%s,%s)"  # Guardar Árboles completos de URLs.

    for urlstree in URLs:
        urljsonstr = json.dumps(urlstree).replace(' ', '')
        print(urljsonstr)
        sqlPD.write(sqlWrite, (hash(urljsonstr), urljsonstr))
'''
if __name__ == '__main__':
    extractContentElements()
