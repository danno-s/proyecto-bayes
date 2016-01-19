#!/usr/bin/python

"""
Calcula histrogramas sobre los usuarios y sus LRS
"""

from src.featureExtraction.featureExtractionUtils import subsequences, isSubContained
from src.utils.sqlUtils import sqlWrapper


def calcUserLRSHistograms():
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    # Lectura de sessions

    sqlRead = 'select idsession, user from sessions'
    rows = sqlPD.read(sqlRead)
    assert len(rows)>0
    userSessions = dict() # (user_id, set of session ids of user).

    for row in rows:
        user_id = row[1]
        if user_id in userSessions:
            userSessions[user_id].append(int(row[0]))
        else:
            sessionIDs = list()
            userSessions[user_id]= sessionIDs
    assert len(userSessions)>0

    # Lectura de sessiondata

    sqlRead = 'select idsession, urls from sessiondata'
    rows = sqlPD.read(sqlRead)
    assert len(rows)>0

    sessionSubseqs = dict() # (idsession, set of subsequences of current session).
    for row in rows:
        urls = str(row[1]).split(' ')
        sessionSubseqs[int(row[0])]=set(subsequences(urls))
    assert len(sessionSubseqs)

    sqlRead = 'select seqs from lrss'
    rows = sqlPD.read(sqlRead)
    assert len(rows)>0

    lrss = [item[0] for item in rows]

    D = dict()
    for user_id,sessionIDs in userSessions.items():
        if user_id in D:
            v = D[user_id]
        else:
            v = [0]*len(lrss)
        for session_id in sessionIDs:
            seq = sessionSubseqs[session_id]
            for i,lrs in enumerate(lrss):
               if isSubContained(lrs,seq):
                    v[i] += 1
        D[user_id] = v
    assert len(D)>0

    counts = dict()
    for i,key in enumerate(D.keys()):
        N = sum(D[key])
        if N != 0:
            D[key] = [val/N for val in D[key]]
        counts[key] = N
    assert len(counts)>0

    for key,val in D.items():
        D[key]= ' '.join([str("%.4f"%(x)) for x in val])

    for k,v in D.items():
        print(str(k)+", "+str(v))

    sqlPD.truncate('userlrshistograms')

    sqlWrite = "INSERT INTO userlrshistograms (id_usuario,lrshistogram,frequency) VALUES (%s, %s,%s)"

    for k,v in D.items():
        sqlPD.write(sqlWrite, (k,v,counts[k]))

if __name__ == '__main__':
    calcUserLRSHistograms()