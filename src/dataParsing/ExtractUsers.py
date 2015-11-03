#!/usr/bin/python

import json
import mysql.connector


with open('connections.json', 'r') as f:
	connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connRead = connections[0]
connWrite = connections[1]

#print(connRead)
#print(connWrite)

sqlRead = 'select * from pageview'
cnx = mysql.connector.connect(user=connRead['user'], password=connRead['passwd'], host=connRead['host'],database=connRead['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
rows = cursor.fetchall()

L = set()

for row in rows:
    l = row[5].split(";")
    L.add((int(l[3][l[3].rfind(":")+2:-1]),l[1][l[1].rfind(":")+1:],l[5][l[5].rfind(":")+1:]))

print(L)

cnx.close()

sqlWrite = ("INSERT INTO users (id_usuario,username,perfil) VALUES (%s, %s, %s)")

cnx = mysql.connector.connect(user=connWrite['user'], password=connWrite['passwd'], host=connWrite['host'],database=connWrite['db'])
cursor = cnx.cursor()

for item in L:
	sql = sqlWrite + '"' + str(item) + '"'
	print(sql)
	cursor.execute(sqlWrite,item)

cnx.commit()
cnx.close()