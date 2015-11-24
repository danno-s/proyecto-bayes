#!/usr/bin/python

import json
import mysql.connector

tlimit = 100

def indexinsert(l, t):
    for i in range(l.length()):
        if l[i][1] > t :
            return i
    return l.length()

def insesion(l, t):
    if t - l[-1][1] <= tlimit :
        return True
    else: return False



with open('connections.json', 'r') as f:
	connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0]
connPD = connections[1]


sqlRead = 'select url, variables, clickDate from pageview'
cnx = mysql.connector.connect(user=connGC['user'], password=connGC['passwd'], host=connGC['host'],database=connGC['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
pageview = cursor.fetchall()

cnx.close()

print(pageview)

cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

# urls = [str(item[0]) for item in urls]

userL = list()
L = list()

for row in pageview:
    l = row[1].split(";")
    id = int(l[3][l[3].rfind(":")+2:-1])
    tstamp = int(row[2])
    l = row[0].split(" ")
    l = l[0]
    if id in userL:
        idxs = [i for i,x in enumerate(userL) if x==id]
        for i in idxs:
            if insesion(L[i],tstamp):
                L[i].insert(indexinsert(L[i],tstamp),(l,tstamp))
                break
    else:
        userL.append(id)
        L.append(list((l,tstamp)))

print(userL)
print(L)



# for key in D.keys():
#     D[key] = str(tuple(D[key]))
#
# print(D)
#
# sqlWrite = ("INSERT INTO userclusteringfeatures (id_usuario,userFeatureVector) VALUES (%s, %s)")
#
# for item in D.items():
# 	cursor.execute(sqlWrite,item)
#
# cnx.commit()
# cnx.close()