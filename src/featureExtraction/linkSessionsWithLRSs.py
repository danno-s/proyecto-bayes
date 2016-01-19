#!/usr/bin/python

from src.featureExtraction.featureExtractionUtils import subsequences, isSubContained
from src.utils.sqlUtils import sqlWrapper

def linkSessionsWithLRSs():
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    # Lectura de sessiondata

    sqlRead = 'select idsession, urls from sessiondata'
    rows = sqlPD.read(sqlRead)
    assert len(rows)>0

    sessionSubseqs = dict() # (idsession, set of subsequences of current session).
    for row in rows:
        urls = str(row[1]).split(' ')
        sessionSubseqs[int(row[0])]=set(subsequences(urls))

    assert len(sessionSubseqs)>0

    sqlRead = 'select seqs from lrss'
    rows = sqlPD.read(sqlRead)
    assert len(rows)>0

    lrss = [item[0] for item in rows]

    D = dict()

    for session_id,seq in sessionSubseqs.items():
        if session_id in D:
            v = D[session_id]
        else:
            v = [0]*len(lrss)
        for i,lrs in enumerate(lrss):
            if isSubContained(lrs,seq):
                v[i] = 1
        D[session_id] = v

    assert len(D)>0

    for k,v in D.items():
        print(str(k)+", "+str(v))

    for key,val in D.items():
        D[key] = ' '.join([str(i) for i in val])

    sqlPD.truncate('sessionlrssfeatures')

    sqlWrite = ("INSERT INTO sessionlrssfeatures (idsession,sessionFeatureVector) VALUES (%s, %s)")

    for k,v in D.items():
        sqlPD.write(sqlWrite,(k,v))

if __name__ == '__main__':
    linkSessionsWithLRSs()