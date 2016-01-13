#!/usr/bin/python

import json
import mysql.connector
import itertools
import os



def consecutive(indices, repeat):
    for i in indices[:-repeat+1]:
        yield tuple(x for x in range(i,i+repeat))

def subsequences(iterable):
    pool=tuple(iterable)
    n= len(pool)
    if n > 1:
        for r in range(2,n):
            inGen = (x for x in consecutive(range(n), repeat=r))
            for indices in inGen:
                yield ' '.join(tuple(pool[i] for i in indices))

    yield ' '.join(pool)

def subsequence(item):
    pool=tuple(item)
    n= len(pool)
    if n > 1:
        for r in range(2,n):
            inGen = (x for x in consecutive(range(n), repeat=r))
            for indices in inGen:
                yield ' '.join(tuple(pool[i] for i in indices))
    yield ' '.join(pool)

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
sessionSubseqs = dict() # (idsession, set of subsequences of current session).
for row in rows:
    urls = str(row[1]).replace('[','').replace(']','').replace(',','').split(' ')
    for ss in subsequences(urls):
        allsubseqsL.append(ss)
    sessionSubseqs[int(row[0])]=set(subsequence(urls))

#for ss in sorted(allsubseqsL):
#    print(ss)

print("Buscando LRSs para un total de " + str(len(allsubseqsL)) + " subsecuencias.")

# Lectura de sessions

sqlRead = 'select idsession, user from sessions'
cursor.execute(sqlRead)
rows = cursor.fetchall()
userD = dict() # (idsession,user)
for row in rows:
    userD[int(row[0])]=row[1]

# print(userD)
# print(sessionSubseqs)

## Calcular LRSs
mode = 'COUNT_SUBSEQS'
if mode is 'COUNT_SPAM_USER':
    # Identificar secuencias y contar repeticiones de cada una.
    #   [Sin discriminar secuencias repetidas por un mismo usuario]

    Seqs = dict() # (urlseq, count)
    for urlseq in allsubseqsL:
        if urlseq not in Seqs:
            Seqs[urlseq] = 1
        else:
            Seqs[urlseq] += 1
elif mode is 'COUNT_SUBSEQS':
    # Identificar subsecuencias y contar repeticiones de cada una.
    #   [Sin discriminar secuencias repetidas por un mismo usuario]
    #   [Considera subsequencias]
    Seqs = dict() # (urlseq, count)
    for seq in allsubseqsL:
        for k,v in sessionSubseqs.items():
            if seq not in Seqs:
                Seqs[seq] = 1
            elif seq in sessionSubseqs[k]:
                    Seqs[seq] += 1
else:
    # Identificar secuencias y contar repeticiones de cada una.
    #   [Discrimina secuencias repetidas por un mismo usuario]

    Seqs = dict() # (urlseq, count)
    userSeqs = dict() #(urlseq, [users])

    for urlseq,id in zip(allsubseqsL, sessionSubseqs.keys()):
        if urlseq not in Seqs:
            Seqs[urlseq] = 0
            userSeqs[urlseq]= [userD[id]]
        elif userD[id] not in userSeqs[urlseq]:
            userSeqs[urlseq].append(userD[id])

    for urlseq in Seqs.keys():
        Seqs[urlseq] = len(userSeqs[urlseq])

#    print(userSeqs)
#print(Seqs)

# Aplicar criterio de repeticiones sobre umbral T
T= 20
RepSeqs = list() # [[urlseq]]
for seq in Seqs:
    if Seqs[seq] > T:
       RepSeqs.append(seq)

print("Subsequences repeated > " + str(T) + " :\n" + str(RepSeqs))


## Funcion que verifica si una subsecuencia 'shortest' esta contenida dentro de la subsecuencia 'longest'.
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


def isSubContained(item, iterable):
    for i,val in enumerate(iterable):
        if contains(item,val):
            return True
    return False

# Eliminar subsecuencias contenidas dentro de otras.
LRSs = RepSeqs.copy()
if len(RepSeqs)>1: # Casos con mas de una subsequencia repetida.
    for i,val in enumerate(sorted(LRSs)):
        if isSubContained(val,LRSs) and val in LRSs:
            LRSs.remove(val)

print("Longest Repeated Subsequences:\n " + str(LRSs))
print("Accessed "+ str([Seqs[lrs] for lrs in LRSs])+ " times.")

# Construir tabla para LRSs en la base de datos

sqlWrite = ("INSERT INTO lrss (seqs,count) VALUES (%s,%s)")

for seq in LRSs:
    cursor.execute(sqlWrite,(seq,Seqs[seq]))
cnx.commit()
cnx.close()


