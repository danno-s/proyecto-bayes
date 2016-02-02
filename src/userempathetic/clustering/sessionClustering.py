import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from matplotlib import pyplot as plt


def getCentroid(cluster):
    N = len(cluster[0])
    return [sum([value[x]/len(cluster) for value in cluster]) for x in range(N)]


def getMax(cluster):
    N = len(cluster[0])
    return [max([value[x] for value in cluster]) for x in range(N)]


def getMin(cluster):
    N = len(cluster[0])
    return [min([value[x] for value in cluster]) for x in range(N)]


def sessionClustering():

    sqlFT = sqlWrapper(db='FT')
    sessionLRSfeats = dict()
    sqlRead = ('select session_id,vector from sessionlrsbelongingfeatures')
    rows= sqlFT.read(sqlRead)
    assert len(rows)>0
    for row in rows:
        sessionLRSfeats[int(row[0])]=[int(x) for x in row[1].split(' ')]

    X= [x for x in sessionLRSfeats.values()]
    M = len(X[0]) # Dimension of feature vector.
    #print(X)

    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.5, min_samples=5,metric='euclidean').fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    #print(labels)

    unique_labels = set(labels)

    #print(core_samples_mask)
    clusteredData = dict()
    for k in unique_labels:
        #   print('LABEL=' + str(k))
        if k == -1:
        #print('k=' + str(k)+' is noise...')
            pass
        else:
            class_member_mask = (labels == k)
            xy=[x for x,i,j in zip(X,class_member_mask,core_samples_mask) if i & j]
            clusteredData[k]=xy

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #print(clusteredData)
    print('Estimated number of clusters: %d' % n_clusters_)
    for k,v in clusteredData.items():
        print("Cluster "+ str(k)+",\t"+str(len(v))+" elementos:\n"+ str(v))



    if len(clusteredData) > 1:
        f, ax = plt.subplots(n_clusters_, sharex=True, sharey=True)

        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        f.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        for k,v in clusteredData.items():
            low = getMin(v)
            c = getCentroid(v)
            up = getMax(v)
            idx = range(M)
            ax[k].plot(idx,low,'g.')
            ax[k].plot(idx,up,'r.')
            ax[k].plot(idx,c,'b.',markersize=10)

        plt.xlim([-0.2,M-1+0.2])
        plt.yticks([0, 1])
        plt.margins(0.2)
        plt.xlabel("LRSs index.")
        ax[n_clusters_/2].set_ylabel("Utilización del LRS")
        ax[0].set_title("Uso de LRSs por sesión representativa de cada cluster")
        plt.show()


if __name__ == '__main__':
    sessionClustering()