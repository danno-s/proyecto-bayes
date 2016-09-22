# -*- coding: utf-8 -*-

from src.clustering.clusterings.Clustering import UserClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.utils.sqlUtils import sqlWrapper
from src.clusterClass.Cluster import Cluster


class UserMacroStatesBelongingClustering(UserClustering):
    """
    Clase UserMacroStatesBelongingClustering implementa un UserClustering que
    realiza clustering utilizando el feature UserMacroStatesBelongingFeature.

    See Also
        UserMacroStatesBelongingFeature
    """
    xlabel = "Macro Estados IDs"
    ylabel = "Utilizacion de Macro Estados"
    title = "Uso de Macro Estados por usuario representativo de cada cluster"

    def __init__(self, confD=None, onlySimulated=False):
        """Constructor

        Returns
        -------

        """
        UserClustering.__init__(self, confD=confD)
        self.onlySimulated = onlySimulated

    def initClusteringAlgorithm(self):
        return DBSCAN(
            eps=self.confD['eps'],
            min_samples=self.confD['min_samples'],
            metric=self.confD['metric'])

    @classmethod
    def getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = \
            'select user_id,vector from userfeatures where feature_name = '\
            "'UserMacroStatesBelonging'"
        sqlRead += " and simulated = 1"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([int(x) for x in row[1].split(' ')])
        return X, ids
