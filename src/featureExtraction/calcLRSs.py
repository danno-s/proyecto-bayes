#!/usr/bin/python

"""
Calcula las LRS (Longuest repeating sequence) en las sesiones
"""

from src.utils.featureExtractionUtils import subsequences, isSubContained
from src.utils.loadConfig import Config
from src.utils.sqlUtils import sqlWrapper


def calcLRSs():

    sqlPD = sqlWrapper(db='PD')            # Asigna las bases de datos que se accederán

    # Lectura de sessiondata
    sqlRead = 'select idsession, urls from sessiondata'
    rows = sqlPD.read(sqlRead)

    allsubseqsL = list()  # urls subsequences of all sessions.
    fullseqsL = list() # sequences of all sessions.
    sessionSubseqs = dict() # (idsession, set of subsequences of current session).
    for row in rows:
        urls = str(row[1]).split(' ')
        fullseqsL.append(row[1])
        for ss in subsequences(urls):
            allsubseqsL.append(ss)
        sessionSubseqs[int(row[0])]=set(subsequences(urls))

    assert len(sessionSubseqs) > 0
    assert len(allsubseqsL) > 0
    assert len(sessionSubseqs) > 0

    # Lectura de sessions
    sqlRead = 'select idsession, user from sessions'
    rows= sqlPD.read(sqlRead)

    userD = dict() # (idsession,user)
    for row in rows:
        userD[int(row[0])]=row[1]

    assert len(userD) > 0

    Seqs = dict() # (urlseq, count)

    ## Calcular LRSs

    mode = 'COUNT_SUBSEQS'     #'COUNT_UNIQUE_USER' | 'COUNT_SPAM_USER' | 'COUNT_SUBSEQS'

    if mode is 'COUNT_SPAM_USER':
        # Identificar secuencias y contar repeticiones de cada una.
        #   [Sin discriminar secuencias repetidas por un mismo usuario]

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
        for seq in allsubseqsL:
            for k,v in sessionSubseqs.items():
                if seq not in Seqs:
                    Seqs[seq] = 1
                elif seq in sessionSubseqs[k]:
                        Seqs[seq] += 1

    elif mode is 'COUNT_UNIQUE_USER':
        # Identificar secuencias y contar repeticiones de cada una.
        #   [Discrimina secuencias repetidas por un mismo usuario]

        userSeqs = dict() #(urlseq, [users])

        for urlseq,id in zip(fullseqsL, sessionSubseqs.keys()):
            if urlseq not in Seqs:
                Seqs[urlseq] = 0
                userSeqs[urlseq]= [userD[id]]
            elif userD[id] not in userSeqs[urlseq]:
                userSeqs[urlseq].append(userD[id])

        for urlseq in Seqs.keys():
            Seqs[urlseq] = len(userSeqs[urlseq])

    assert len(Seqs) > 0

    # Aplicar criterio de repeticiones sobre umbral T


    T= Config().getValue(attr='LRS_threshold',mode='INT')
    assert T > 0

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
    sqlPD.truncate("lrss")

    # Guardar nueva info.

    sqlWrite = ("INSERT INTO lrss (seqs,count) VALUES (%s,%s)")
    for seq in LRSs:
        sqlPD.write(sqlWrite,(seq,Seqs[seq]))


if __name__ == '__main__':
    calcLRSs()