#!/usr/bin/python

import json
import mysql.connector
import os

# Genera tuplas de tamaño 'repeat' con los índices consecutivos extraidos de 'indices'.
def consecutiveIdxs(indices, repeat):
    for i in indices[:-repeat+1]:
        yield tuple(x for x in range(i,i+repeat))

# Generador de las subsecuencias posibles a partir de una sesión.
def subsequences(iterable):
    pool=tuple(iterable)
    n= len(pool)
    if n > 1:
        for r in range(2,n):
            inGen = (x for x in consecutiveIdxs(range(n), repeat=r))
            for indices in inGen:
                yield ' '.join(tuple(pool[i] for i in indices))

    yield ' '.join(pool)

# Funcion que verifica si una subsecuencia 'shortest' esta contenida dentro de la subsecuencia 'longest'.
# Si son iguales, retorna False.


def contains(shortest, longest):
    if shortest == longest:
        return False
    for i in range(len(longest)-len(shortest)+1):
        for j in range(len(shortest)):
            if longest[i+j] != shortest[j]:
                break
        else:
            return True
    return False

# Funcion que verifica si una secuencia 'item' esta subcontenida dentro de algun elemento
# de la lista de secuencias 'iterable'.


def isSubContained(item, iterable):
    for i,val in enumerate(iterable):
        if contains(item,val):
            return True
    return False


with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
    connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0]
connPD = connections[1]


# Lectura de sessiondata
sqlRead = 'select idsession, urls from sessiondata'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()
cursor.execute(sqlRead)
rows = cursor.fetchall()

sessionSubseqs = dict() # (idsession, set of subsequences of current session).
urlsFull=dict()
for row in rows:
    urls = str(row[1]).replace('[','').replace(']','').replace(',','').split(' ')
    sessionSubseqs[int(row[0])]=set(subsequences(urls))
    urlsFull[int(row[0])]=urls

sqlRead = 'select seqs from lrss'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
rows = cursor.fetchall()
#lrs_id =[item[0] for item in rows]
lrss = [item[0] for item in rows]

D = dict()

for session_id,seq in sessionSubseqs.items():
    if session_id in D:
        v = D[session_id]
    else:
        v = [0]*len(lrss)
    for i,lrs in enumerate(lrss):
        if isSubContained(lrs,seq):
            print("SESION: "+ str(session_id)+", " + str(lrs) + ' in ' + str(urlsFull[session_id]))
            v[i] = 1
    D[session_id] = v

#for k,v in D.items():
#    print(str(k)+", "+str(v))
#    if sum(v)==0:
#        print(urlsFull[k])

for key,val in D.items():
    D[key] = ' '.join([str(i) for i in val])

cursor.execute("TRUNCATE sessionlrssfeatures")

sqlWrite = ("INSERT INTO sessionlrssfeatures (idsession,sessionFeatureVector) VALUES (%s, %s)")

for k,v in D.items():
    print(str(sqlWrite)+", " + str((k,v)))
    cursor.execute(sqlWrite,(k,v))

cnx.commit()
cnx.close()