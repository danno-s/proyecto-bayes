#!/usr/bin/python

import json
import mysql.connector
import itertools

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
T= 20
RepSeqs = list() # [[urlseq]]
for urlseq in Seqs:
    if Seqs[urlseq] > T:
       RepSeqs.append(urlseq.split(" "))

print("Subsequences repeated > " + str(T) + " :" + str(RepSeqs))


## Funcion que verifica si una subsecuencia 'shortest' esta contenida dentro de la subsecuencia 'longest'.


def contains(shortest, longest):
    for i in range(len(longest)-len(shortest)+1):
        for j in range(len(shortest)):
            if longest[i+j] != shortest[j]:
                break
        else:
            return True
    return False

# Eliminar subsecuencias contenidas dentro de otras.

LRSs = list()
if len(RepSeqs)<=1: # Casos con una o ninguna subsequencia repetida.
    LRSs = RepSeqs.copy()
else:
    for i,j in itertools.permutations(RepSeqs,2):
        # print("i = " +str(i)+ " j = " + str(j))
        # print(contains(i,j))
        if contains(i,j):
            if not LRSs.__contains__(j):
                LRSs.append(j)

print("Longest Repeated Subsequences: " + str(LRSs))

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