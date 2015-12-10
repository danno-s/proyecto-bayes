#!/usr/bin/python

import json
import mysql.connector

with open('connections.json', 'r') as f:
    connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0] #guideCapture
connPD = connections[1] #parsedData

# Lectura de URLsesions
sqlRead = 'select idsesion, urls from urlsesions'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
rows = cursor.fetchall()
L = list()  # urls sequences
idL = list() # idsesions
for row in rows:
    idL.append(int(row[0]))
    L.append(row[1])

# print(idL)
# print(L)

## Calcular LRSs

# Identificar secuencias y contar repeticiones de cada una.
Seqs = dict() # (urlseq, count)
for urlseq in L:
    if urlseq not in Seqs:
        Seqs[urlseq] = 1
    else:
        Seqs[urlseq] += 1

print(Seqs)

# Aplicar criterio de repeticiones sobre umbral T
T= 15
RepSeqs = list() # [[urlseq]]
for urlseq in Seqs:
    if Seqs[urlseq] > T:
       RepSeqs.append(urlseq.split(" "))

print("repseqs > " + str(T) + ":")
print(RepSeqs)

# TODO: Eliminar subsecuencias contenidas dentro de otras.
# Investigar Suffix Trees (Most common substring problem)

# LRSs = list()
# for urlseq in RepSeqs:
#     pass
# print("LRSs:")
# print(LRSs)

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