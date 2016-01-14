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


# Extraer datos de conexión a DB.
with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
	connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0] #guideCapture
connPD = connections[1] #parsedData

# Lectura de sessiondata
sqlRead = 'select idsession, urls from sessiondata'
cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()
cursor.execute(sqlRead)
rows = cursor.fetchall()

allsubseqsL = list()  # urls subsequences of all sessions.
fullseqsL = list() # sequences of all sessions.
sessionSubseqs = dict() # (idsession, set of subsequences of current session).
for row in rows:
    urls = str(row[1]).replace('[','').replace(']','').replace(',','').split(' ')
    fullseqsL.append(' '.join(urls))
    for ss in subsequences(urls):
        allsubseqsL.append(ss)
    sessionSubseqs[int(row[0])]=set(subsequences(urls))

# Lectura de sessions

sqlRead = 'select idsession, user from sessions'
cursor.execute(sqlRead)
rows = cursor.fetchall()
userD = dict() # (idsession,user)
for row in rows:
    userD[int(row[0])]=row[1]

## Calcular LRSs
mode = 'COUNT_SUBSEQS'     #'COUNT_UNIQUE_USER' | 'COUNT_SPAM_USER' | 'COUNT_SUBSEQS'

if mode is 'COUNT_SPAM_USER':
    # Identificar secuencias y contar repeticiones de cada una.
    #   [Sin discriminar secuencias repetidas por un mismo usuario]

    Seqs = dict() # (urlseq, count)
    for urlseq in fullseqsL:
        if urlseq not in Seqs:
            Seqs[urlseq] = 1
        else:
            Seqs[urlseq] += 1

elif mode is 'COUNT_SUBSEQS':
    # Identificar subsecuencias y contar repeticiones de cada una.
    #   [Sin discriminar secuencias repetidas por un mismo usuario]
    #   [Considera subsequencias]

    print("Buscando LRSs para un total de " + str(len(allsubseqsL)) + " subsecuencias.")
    Seqs = dict() # (urlseq, count)
    for seq in allsubseqsL:
        for k,v in sessionSubseqs.items():
            if seq not in Seqs:
                Seqs[seq] = 1
            elif seq in sessionSubseqs[k]:
                    Seqs[seq] += 1

elif mode is 'COUNT_UNIQUE_USER':
    # Identificar secuencias y contar repeticiones de cada una.
    #   [Discrimina secuencias repetidas por un mismo usuario]

    Seqs = dict() # (urlseq, count)
    userSeqs = dict() #(urlseq, [users])

    for urlseq,id in zip(fullseqsL, sessionSubseqs.keys()):
        if urlseq not in Seqs:
            Seqs[urlseq] = 0
            userSeqs[urlseq]= [userD[id]]
        elif userD[id] not in userSeqs[urlseq]:
            userSeqs[urlseq].append(userD[id])

    for urlseq in Seqs.keys():
        Seqs[urlseq] = len(userSeqs[urlseq])

# Aplicar criterio de repeticiones sobre umbral T


T= 20   # PARÁMETRO DEL ALGORITMO.


RepSeqs = list() # [[urlseq]]
for seq in Seqs:
    if Seqs[seq] > T:
       RepSeqs.append(seq)

print("Subsequences repeated > " + str(T) + " :\n" + str(RepSeqs))

# Eliminar subsecuencias contenidas dentro de otras.
LRSs = RepSeqs.copy()
if len(RepSeqs)>1: # Casos con mas de una subsequencia repetida.
    for i,val in enumerate(sorted(LRSs)):
        if isSubContained(val,LRSs) and val in LRSs:
            LRSs.remove(val)

print("Longest Repeated Subsequences:\n " + str(LRSs))
print("Accessed: \n"+ str([Seqs[lrs] for lrs in LRSs])+ " times.")

# Completar tabla para LRSs en la base de datos

# Resetear lrss
cursor.execute("TRUNCATE lrss")

# Guardar nueva info.

sqlWrite = ("INSERT INTO lrss (seqs,count) VALUES (%s,%s)")

for seq in LRSs:
    cursor.execute(sqlWrite,(seq,Seqs[seq]))
cnx.commit()
cnx.close()


