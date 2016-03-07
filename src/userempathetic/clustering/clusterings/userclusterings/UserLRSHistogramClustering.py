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
    """Clase UserLRSHistogramClustering implementa un UserClustering que realiza clustering utilizando
    el feature UserLRSHistogramFeature.

    See Also
        UserLRSHistogramFeature
    """
    xlabel = "LRSs IDs"
    ylabel = "Frecuencia relativa del LRS"
    title = "Histograma de LRSs de usuario representativo de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        UserClustering.__init__(self)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=0.7, min_samples=5, metric='euclidean')

    @classmethod
    def getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select user_id,vector from userfeatures where feature_name = '+"'UserLRSHistogram'"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([float(x) for x in row[1].split(' ')])
        return X, ids


