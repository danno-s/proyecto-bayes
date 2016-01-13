#!/usr/bin/python

import json
import mysql.connector
import hashlib
import os
from phpserialize import *

def hash(string):
    return hashlib.md5(string.encode()).hexdigest()


with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
	connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0]
connPD = connections[1]


sqlRead = 'select urls, variables from pageview'
cnx = mysql.connector.connect(user=connGC['user'], password=connGC['passwd'], host=connGC['host'],database=connGC['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
usersUrls = cursor.fetchall()

cnx.close()

sqlRead = 'select id from urls'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
urls = cursor.fetchall()

urls = [item[0] for item in urls]

D = dict()

for row in usersUrls:
    l = loads(bytes(row[1], 'UTF-8'))
    try:
        id = int(l[b'id_usuario'].decode("utf-8"))
        l = hash(json.dumps(json.loads(row[0])))
        if id in D:
            v = D[id]
        else:
            v = [0]*len(urls)
        for i in range(len(urls)):
            if urls[i] == l: #PORQUE NO SON IGUALES!!!!!!!!!!!!!!!
                v[i] = 1
        D[id] = v
    except TypeError:
        print("Texto no corresponde a datos de usuario, variable leida = "+str(l))

for key in D.keys():
    D[key] = str(tuple(D[key]))

cursor.execute("TRUNCATE userclusteringfeatures")

sqlWrite = ("INSERT INTO userclusteringfeatures (id_usuario,userFeatureVector) VALUES (%s, %s)")

for item in D.items():
	cursor.execute(sqlWrite,item)

cnx.commit()
cnx.close()