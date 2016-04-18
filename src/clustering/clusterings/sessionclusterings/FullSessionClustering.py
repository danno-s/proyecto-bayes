from src.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.clusterClass.Cluster import Cluster
from src.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import SessionUserClustersBelongingClustering
from src.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering


class FullSessionClustering(SessionClustering):
    """
    Clase FullSessionClustering implementa un SessionClustering que realiza clustering utilizando
    todos los features de sesiones, concatenados en un mismo vector.
    """
    xlabel = "Dimensiones"
    ylabel = "Valor"
    title = "Valores en cada dimensión de sesión representativa de cada cluster"

    def __init__(self, confD=None):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self, confD=confD)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=self.confD['eps'], min_samples=self.confD['min_samples'], metric=self.confD['metric'])

    def getData(self):
        X_lrs, ids = SessionLRSBelongingClustering.getData()
        X_url, _ = SessionUserClustersBelongingClustering.getData()
        X = list()
        for i, user_id in enumerate(ids):
            vector = []
            if X_lrs is not None:
                vector.extend(X_lrs[i])
            if X_url is not None:
                vector.extend(X_url[i])
            X.append(vector)

        return X, ids
