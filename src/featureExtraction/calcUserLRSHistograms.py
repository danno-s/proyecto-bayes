#!/usr/bin/python

"""
Calcula histrogramas sobre los usuarios y sus LRS
"""

from src.featureExtraction.featureExtractionUtils import subsequences, isSubContained
from src.utils.sqlUtils import sqlWrapper


def calcUserLRSHistograms():
    sqlPD = sqlWrapper(db='PD')


    # Lectura de sessions

    sqlRead = 'select idsession, user from sessions'
    rows = sqlPD.read(sqlRead)
    userSessions = dict() # (user_id, set of session ids of user).

    for row in rows:
        user_id = row[1]
        if user_id in userSessions:
            userSessions[user_id].append(int(row[0]))
        else:
            sessionIDs = list()
            userSessions[user_id]= sessionIDs

    sessionSubseqs = dict() # (idsession, set of subsequences of current session).
    for row in rows:
        urls = str(row[1]).split(' ')
        sessionSubseqs[int(row[0])]=set(subsequences(urls))


    # Lectura de sessiondata

    sqlRead = 'select idsession, urls from sessiondata'
    rows = sqlPD.read(sqlRead)

    sessionSubseqs = dict() # (idsession, set of subsequences of current session).
    for row in rows:
        urls = str(row[1]).split(' ')
        sessionSubseqs[int(row[0])]=set(subsequences(urls))

    sqlRead = 'select seqs from lrss'
    rows = sqlPD.read(sqlRead)

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

    N = 0
    for vals in D.values():
        for val in vals:
            N += val
    for key,val in D.items():
        D[key] = ' '.join([str("%.4f"%(i/N)) for i in val])

    for k,v in D.items():
        print(str(k)+", "+str(v))

    sqlPD.truncate('userlrshistograms')

    sqlWrite = ("INSERT INTO userlrshistograms (id_usuario,lrshistogram) VALUES (%s, %s)")

    for k,v in D.items():
        sqlPD.write(sqlWrite,(k,v))

if __name__ == '__main__':
    calcUserLRSHistograms()