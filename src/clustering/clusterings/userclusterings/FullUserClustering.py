# -*- coding: utf-8 -*-

from src.clustering.clusterings.Clustering import UserClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.utils.sqlUtils import sqlWrapper
from src.clusterClass.Cluster import Cluster
from src.utils.dataParsingUtils import getAllUserIDs
from src.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
from src.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering


class FullUserClustering(UserClustering):
    """Clase UserURLsBelongingClustering implementa un UserClustering que realiza clustering utilizando
    el feature UserURLsBelongingFeature.

    See Also
        UserURLsBelongingFeature
    """
    xlabel = "Dimensiones"
    ylabel = "Valor"
    title = "Valores en cada dimensión de usuario representativo de cada cluster"

    def __init__(self, confD=None):
        """Constructor

        Returns
        -------

        """
        UserClustering.__init__(self, confD=confD)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=self.confD['eps'], min_samples=self.confD['min_samples'], metric=self.confD['metric'])

    def getData(self):
        X_lrs, ids = UserLRSHistogramClustering.getData()
        X_url, _ = UserURLsBelongingClustering.getData()
        X = list()
        for i, user_id in enumerate(ids):
            vector = []
            if len(X_lrs) > 0:
                vector.extend(X_lrs[i])
            if len(X_url) > 0:
                vector.extend(X_url[i])
            X.append(vector)

        return X, ids


if __name__ == '__main__':
    fuc = FullUserClustering()
    print(fuc.featuresDIM)
    print(UserLRSHistogramClustering().featuresDIM)
    print(UserURLsBelongingClustering().featuresDIM)
