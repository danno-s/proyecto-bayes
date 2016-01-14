#!/usr/bin/python

from src.featureExtraction.featureExtractionUtils import subsequences, isSubContained
from src.sqlUtils.sqlUtils import sqlWrapper

sqlPD = sqlWrapper(db='PD')

# Lectura de sessiondata

sqlRead = 'select idsession, urls from sessiondata'
rows = sqlPD.read(sqlRead)

sessionSubseqs = dict() # (idsession, set of subsequences of current session).
urlsFull=dict()
for row in rows:
    urls = str(row[1]).replace('[','').replace(']','').replace(',','').split(' ')
    sessionSubseqs[int(row[0])]=set(subsequences(urls))
    urlsFull[int(row[0])]=urls

sqlRead = 'select seqs from lrss'
rows = sqlPD.read(sqlRead)
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

sqlPD.truncate('sessionlrssfeatures')

sqlWrite = ("INSERT INTO sessionlrssfeatures (idsession,sessionFeatureVector) VALUES (%s, %s)")

for k,v in D.items():
    sqlPD.write(sqlWrite,(k,v))