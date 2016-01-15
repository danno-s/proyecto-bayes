#!/usr/bin/python

import json
import hashlib
from src.utils.sqlUtils import sqlWrapper

from phpserialize import *

def hash(string):
    return hashlib.md5(string.encode()).hexdigest()

sqlGC = sqlWrapper(db='GC')
sqlPD = sqlWrapper(db='PD')

sqlRead = 'select urls, variables from pageview'
usersUrls = sqlGC.read(sqlRead)

sqlRead = 'select id from urls'
urls = sqlPD.read(sqlRead)

urls = [item[0] for item in urls]

D = dict()

for row in usersUrls:
    l = loads(bytes(row[1], 'UTF-8'))
    try:
        id = int(l[b'id_usuario'].decode("utf-8"))
        l = hash(json.dumps(json.loads(row[0])).replace(' ', ''))
        if id in D:
            v = D[id]
        else:
            v = [0]*len(urls)
        for i in range(len(urls)):
            if urls[i] == l:
                v[i] = 1
        D[id] = v
    except TypeError:
        print("Texto no corresponde a datos de usuario, variable leida = "+str(l))

for key,val in D.items():
    D[key] = ' '.join([str(i) for i in val])

sqlPD.truncate("userclusteringfeatures")

sqlWrite = ("INSERT INTO userclusteringfeatures (id_usuario,userFeatureVector) VALUES (%s, %s)")

for item in D.items():
	sqlPD.write(sqlWrite,item)
