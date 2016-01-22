import numpy as np
from sklearn.cluster import DBSCAN
from src.utils.sqlUtils import sqlWrapper
from matplotlib import pyplot

def sessionClustering():

    sqlPD = sqlWrapper(db='PD')
    sessionLRSfeats = dict()
    sqlRead = ('select idsession,sessionFeatureVector from sessionlrssfeatures')
    rows= sqlPD.read(sqlRead)
    assert len(rows)>0
    for row in rows:
        sessionLRSfeats[int(row[0])]=[int(x) for x in row[1].split(' ')]

    print(sessionLRSfeats)
    X= [x for x in sessionLRSfeats.values()]
    print(X)

    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.5, min_samples=2,metric='euclidean').fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    print(labels)

    unique_labels = set(labels)

    print(core_samples_mask)
    clusteredData = dict()
    for k in unique_labels:
        print('LABEL=' + str(k))
        if k == -1:
            print('k=' + str(k)+' is noise...')

        else:
            class_member_mask = (labels == k)
            xy=[x for x,i,j in zip(X,class_member_mask,core_samples_mask) if i & j]
            clusteredData[k]=xy
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
   # print(clusteredData)
    print('Estimated number of clusters: %d' % n_clusters_)
    for k,v in clusteredData.items():
        print(str(k)+": "+str(v))


    # TODO: Visualizar info de cluster por variable... centroide, max y min.

    def getCentroid(cluster):
        N = len(cluster[0])
        return [sum([value[x]/len(v) for value in v]) for x in range(N)]
    def getMax(cluster):
        N = len(cluster[0])
        return [max([value[x] for value in v]) for x in range(N)]
    def getMin(cluster):
        N = len(cluster[0])
        return [min([value[x] for value in v]) for x in range(N)]

    data = list()
    for k,v in clusteredData.items():
        low = getMin(v)
        c = getCentroid(v)
        up = getMax(v)
        print(low)
        print(c)
        print(up)
        var = list()
        for i in range(len(c)):
            var.append([low[i],c[i],up[i]])
        varvar = list()
        for i in [0]*3:
            for varInd,H in enumerate(var):
                varvar.append([varInd,H[i]])
        pyplot.plot(varvar)
        pyplot.show()
        print(varvar)

#        print(var)

if __name__ == '__main__':
    sessionClustering()