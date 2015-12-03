#!/usr/bin/python

import json
import mysql.connector

with open('connections.json', 'r') as f:
    connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0] #guideCapture
connPD = connections[1] #parsedData

sqlRead = 'select idsesion, urls from urlsesions'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
rows = cursor.fetchall()
L = list()  # urls
idL = list() # idsesions
for row in rows:
    idL.add(int(row[1]))
    l = row[0].split(" ")
    L.add(l[0])

print(idL)
print(L)

# TODO: Computar LRSs de la lista de sesiones.
# Requiere identificar subsecuencias y contar repeticiones de cada una.
# subseq = set() # Contiene subsequencias mas largas identificadas.
# countsubseq = set()
# Definir condiciones para ser LRS: Repeticiones sobre umbral T, consecutividad, subsecuencia mayor.
# lrss = set()

cnx.close()

# Construir tabla para LRSs en la base de datos(?)
#
#sqlWrite = ("INSERT INTO lrss (seqs) VALUES (%s)")
#
#for seq in lrss:
#	cursor.execute(sqlWrite,seq)
#
#cnx.commit()
#cnx.close()
###