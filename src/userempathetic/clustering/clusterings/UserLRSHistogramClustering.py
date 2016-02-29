"""
Clase SessionLRSBelongingClustering

Crea clusters de uso de LRSs por sesión
"""

from src.userempathetic.clustering.clusterings.Clustering import UserClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.clusterClass.Cluster import Cluster


class UserLRSHistogramClustering(UserClustering):
    tablename = 'userlrshistogramclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid) VALUES (%s,%s,%s)'
    xlabel = "LRSs IDs"
    ylabel = "Frecuencia relativa del LRS"
    title = "Histograma de LRSs de usuario representativo de cada cluster"

    def __init__(self):
        UserClustering.__init__(self)
        self.clusteringAlgorithm = DBSCAN(eps=0.3, min_samples=8, metric='euclidean')
        self.clustersD = dict()
        self.n_clusters = 0
        self.X, self.ids = self.__getData()
        self.featuresDIM = len(self.X[0])  # Dimension of feature vector.

    def clusterize(self):
        # Compute DBSCAN
        self.clusteringAlgorithm.fit(self.X)
        core_samples_mask = np.zeros_like(self.clusteringAlgorithm.labels_, dtype=bool)
        core_samples_mask[self.clusteringAlgorithm.core_sample_indices_] = True
        unique_labels = set(self.clusteringAlgorithm.labels_)
        for k in unique_labels:
            class_member_mask = (self.clusteringAlgorithm.labels_ == k)
            xy = [(x, id) for x, id, i, j in zip(self.X, self.ids, class_member_mask, core_samples_mask) if i & j]
            if k != -1:
                self.clustersD[k] = Cluster(elements=xy, label=k, clusteringType=UserLRSHistogramClustering)
            else:
                print("# outliers = "+ str(len(xy)))
                # if xy:
                #   self.clustersD[k]=Cluster(elements=xy,label=k,clusteringType=SessionLRSBelongingClustering)
                pass
        # Number of clusters in labels, ignoring noise if present.
        self.n_clusters = len(unique_labels)
        if -1 in self.clusteringAlgorithm.labels_:
            self.n_clusters -= 1

    def __getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select user_id,histogram from userlrshistogramfeatures'
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([float(x) for x in row[1].split(' ')])
        return X, ids

    def getClusters(self):
        return self.clustersD
