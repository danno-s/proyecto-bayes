#!/usr/bin/python

import json
import mysql.connector

with open('connections.json', 'r') as f:
    connectionsJSON = f.read()
    
connections = json.loads(connectionsJSON)

conn = connections[0]
print(conn)
sql='select * from pageview'
cnx = mysql.connector.connect(user=conn['user'], password=conn['passwd'], host=conn['host'],database=conn['db'])
cursor = cnx.cursor()

cursor.execute(sql)
rows = cursor.fetchall()

for row in rows:
    print(row[4])
        
cnx.close()