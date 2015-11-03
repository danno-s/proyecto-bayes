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
	L.update(row[4].split(" "))

cnx.close()

sqlWrite = "INSERT INTO urls (url) VALUES ("

cnx = mysql.connector.connect(user=connWrite['user'], password=connWrite['passwd'], host=connWrite['host'],database=connWrite['db'])
cursor = cnx.cursor()

for url in L:
	sql = sqlWrite + '"' + url + '"'
	print(sql)
	cursor.execute(sqlWrite + '"' + url + '");')

cnx.commit()
cnx.close()