# -*- coding: utf-8 -*-

from src.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.utils.sqlUtils import sqlWrapper
from src.clusterClass.Cluster import Cluster


class SessionLRSBelongingClustering(SessionClustering):
    """Clase SessionLRSBelongingClustering implementa un SessionClustering que realiza clustering utilizando
    el feature LRSBelongingFeature.

    See Also
        LRSBelongingFeature
    """
    xlabel = "LRSs IDs"
    ylabel = "Utilizacion del LRS"
    title = "Uso de LRSs por sesion representativa de cada cluster"

    def __init__(self, confD=None):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self, confD=confD)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=self.confD['eps'], min_samples=self.confD['min_samples'], metric=self.confD['metric'])

    @classmethod
    def getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select session_id,vector from sessionfeatures where feature_name = ' + \
            "'SessionLRSBelonging'"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([int(x) for x in row[1].split(' ')])
        return X, ids
