#!/usr/bin/python

import json
import mysql.connector
import os


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

sqlRead = 'select urls from urls'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
urls = cursor.fetchall()
print(urls)

urls = [str(item[0]) for item in urls]

D = dict()

for row in usersUrls:
    l = row[1].split(";")
    id = int(l[3][l[3].rfind(":")+2:-1])
    l = row[0].split(" ")
    if id in D:
        v = D[id]
    else:
        v = [0]*len(urls)
    for i in range(len(urls)):
        if urls[i] in l:
            v[i] = 1
    D[id] = v

for key in D.keys():
    D[key] = str(tuple(D[key]))

print(D)

sqlWrite = ("INSERT INTO userclusteringfeatures (id_usuario,userFeatureVector) VALUES (%s, %s)")

for item in D.items():
	cursor.execute(sqlWrite,item)

cnx.commit()
cnx.close()