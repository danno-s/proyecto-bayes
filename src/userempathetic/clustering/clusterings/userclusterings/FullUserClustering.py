from src.userempathetic.clustering.clusterings.Clustering import UserClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.clusterClass.Cluster import Cluster
from src.userempathetic.utils.dataParsingUtils import getAllUserIDs
from src.userempathetic.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
from src.userempathetic.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering


class FullUserClustering(UserClustering):
    """Clase UserURLsBelongingClustering implementa un UserClustering que realiza clustering utilizando
    el feature UserURLsBelongingFeature.

    See Also
        UserURLsBelongingFeature
    """
    xlabel = "Dimensiones"
    ylabel = "Valor"
    title = "Valores en cada dimensión de usuario representativo de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        UserClustering.__init__(self)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=0.8, min_samples=5, metric='euclidean')

    @classmethod
    def getData(self):
        X_lrs, ids = UserLRSHistogramClustering.getData()
        X_url, _ = UserURLsBelongingClustering.getData()
        X = list()
        for i,user_id in enumerate(ids):
            vector = []
            if len(X_lrs) > 0 :
                vector.extend(X_lrs[i])
            if len(X_url) > 0 :
                vector.extend(X_url[i])
            X.append(vector)

        return X, ids


if __name__ == '__main__':
    fuc = FullUserClustering()
    print(fuc.featuresDIM)
    print(UserLRSHistogramClustering().featuresDIM)
    print(UserURLsBelongingClustering().featuresDIM)
