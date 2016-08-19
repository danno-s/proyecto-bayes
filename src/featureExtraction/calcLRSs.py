#!/usr/bin/python

"""
Calcula las LRS (Longuest repeating sequence) de las sesiones
"""

from src.utils.featureExtractionUtils import subsequences, isSubContained
from src.utils.loadConfig import Config
from src.utils.sqlUtils import sqlWrapper


def calcLRSs():
    """Calcula los LRSs en base a las sesiones extraidas.

    Parameters
    ----------

    Returns
    -------

    """
    # Lectura de sessions
    sqlCD = sqlWrapper(db='CD')  # Asigna las bases de datos que se accederan
    sqlRead = 'select id,profile,sequence,user_id,inittime,endtime from sessions'

    rows = sqlCD.read(sqlRead)

    allsubseqsL = list()  # urls subsequences of all sessions.
    fullseqsL = list()  # sequences of all sessions.
    # (idsession, set of subsequences of current session).
    sessionSubseqs = dict()
    userD = dict()  # (idsession,user)
    for row in rows:
        userD[int(row[0])] = row[3]
        steps = str(row[2]).split(' ')
        fullseqsL.append(row[2])
        for ss in subsequences(steps):
            allsubseqsL.append(ss)
        sessionSubseqs[int(row[0])] = set(subsequences(steps))

    assert len(sessionSubseqs) > 0
    assert len(allsubseqsL) > 0
    assert len(sessionSubseqs) > 0
    assert len(userD) > 0

    Seqs = dict()  # (nodeseq, count)

    # Calcular LRSs

    mode = 'COUNT_SUBSEQS'  # 'COUNT_UNIQUE_USER' | 'COUNT_SPAM_USER' | 'COUNT_SUBSEQS'

    if mode is 'COUNT_SPAM_USER':
        # Identificar secuencias y contar repeticiones de cada una.
        #   [Sin discriminar secuencias repetidas por un mismo usuario]

        for nodeseq in fullseqsL:
            if nodeseq not in Seqs:
                Seqs[nodeseq] = 1
            else:
                Seqs[nodeseq] += 1

    elif mode is 'COUNT_SUBSEQS':
        # Identificar subsecuencias y contar repeticiones de cada una.
        #   [Sin discriminar secuencias repetidas por un mismo usuario]
        #   [Considera subsequencias]

        print("Buscando LRSs para un total de " +
              str(len(allsubseqsL)) + " subsecuencias.")
        for seq in allsubseqsL:
            for k, v in sessionSubseqs.items():
                if seq not in Seqs:
                    Seqs[seq] = 1
                elif seq in sessionSubseqs[k]:
                    Seqs[seq] += 1

    elif mode is 'COUNT_UNIQUE_USER':
        # Identificar secuencias y contar repeticiones de cada una.
        #   [Discrimina secuencias repetidas por un mismo usuario]

        userSeqs = dict()  # (nodeseq, [users])

        for nodeseq, u_id in zip(fullseqsL, sessionSubseqs.keys()):
            if nodeseq not in Seqs:
                Seqs[nodeseq] = 0
                userSeqs[nodeseq] = [userD[u_id]]
            elif userD[u_id] not in userSeqs[nodeseq]:
                userSeqs[nodeseq].append(userD[u_id])

        for nodeseq in Seqs.keys():
            Seqs[nodeseq] = len(userSeqs[nodeseq])

    assert len(Seqs) > 0

    # Aplicar criterio de repeticiones sobre umbral T

    T = Config.getValue(attr='LRS_threshold', mode='INT')
    assert T > 0

    RepSeqs = list()  # [[nodeseq]]
    for seq in Seqs:
        if Seqs[seq] > T:
            RepSeqs.append(seq)

    print("Subsequences repeated > " + str(T) + " :\n" + str(RepSeqs))

    # Eliminar subsecuencias contenidas dentro de otras.
    LRSs = RepSeqs.copy()
    if len(RepSeqs) > 1:  # Casos con mas de una subsequencia repetida.
        for i, val in enumerate(sorted(LRSs)):
            if isSubContained(val, LRSs) and val in LRSs:
                LRSs.remove(val)

    LRSs.sort()
    print("Longest Repeated Subsequences:\n " + str(LRSs))
    print("Accessed: \n" + str([Seqs[lrs] for lrs in LRSs]) + " times.")

    # Completar tabla para LRSs en la base de datos
    # Resetear lrss
    sqlCD.truncate("lrss")

    # Guardar nueva info.

    sqlWrite = "INSERT INTO lrss (sequence,count) VALUES (%s,%s)"
    for seq in LRSs:
        sqlCD.write(sqlWrite, (seq, Seqs[seq]))


if __name__ == '__main__':
    calcLRSs()
