#!/usr/bin/python

"""
Extrae vectores descriptores de los usuarios con respecto a los árboles de URLs
"""

import json
import hashlib
from src.utils.sqlUtils import sqlWrapper



def hash(string):
    """
    Retorna el valor hash de un string, usando MD5

    Parameters
    ----------
    string : string
        El string que se quiere convertir

    Returns
    -------
    string
        El valor del hash
    """
    return hashlib.md5(string.encode()).hexdigest()

def extractUserClusteringFeatures():
    try:
        sqlGC = sqlWrapper(db='GC')
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    sqlRead = 'select urls, variables from pageview'
    usersUrls = sqlGC.read(sqlRead)
    assert len(usersUrls) > 0

    sqlRead = 'select id from urls'
    urls = sqlPD.read(sqlRead)
    assert len(urls)>0

    urls = [item[0] for item in urls]

    D = dict()

    for row in usersUrls:
        l = json.loads(row[1])
        try:
            id = int(l['id_usuario'])
            l = hash(json.dumps(json.loads(row[0])).replace(' ', ''))
            if id in D:
                v = D[id]
            else:
                v = [0] * len(urls)
            for i in range(len(urls)):
                if urls[i] == l:
                    v[i] = 1
            D[id] = v
        except TypeError:
            print("Texto no corresponde a datos de usuario, variable leida = " + str(l))
    assert len(D)>0

    for key, val in D.items():
        D[key] = ' '.join([str(i) for i in val])

    sqlPD.truncate("userclusteringfeatures")

    sqlWrite = ("INSERT INTO userclusteringfeatures (id_usuario,userFeatureVector) VALUES (%s, %s)")

    for item in D.items():
        sqlPD.write(sqlWrite, item)

if __name__ == '__main__':
    extractUserClusteringFeatures()