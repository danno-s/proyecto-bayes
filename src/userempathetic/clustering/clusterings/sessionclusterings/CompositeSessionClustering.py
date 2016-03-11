from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.loadConfig import Config
from src.userempathetic.clusterClass.Cluster import Cluster
from src.userempathetic.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import SessionUserClustersBelongingClustering
from src.userempathetic.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering

class CompositeSessionClustering(SessionClustering):
    """
    Clase FullSessionClustering implementa un SessionClustering que realiza clustering utilizando
    todos los features de sesiones, concatenados en un mismo vector.
    """
    xlabel = "Dimensiones"
    ylabel = "Valor"
    title = "Valores en cada dimensión de sesión representativa de cada cluster"

    def __init__(self,confD=None):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self,confD=confD)


    def initClusteringAlgorithm(self):
        return DBSCAN(eps=self.confD['eps'], min_samples=self.confD['min_samples'], metric=self.confD['metric'])


    def getData(self):
        self.composedFeatures = self.confD['features']
        from src.userempathetic.clustering.ExtractClusters import sessionClusteringsD
        X = list()
        ids = list()
        firstFlag = True
        for cf in self.composedFeatures:
            if cf in sessionClusteringsD.keys():
                if firstFlag:
                    X, ids = sessionClusteringsD[cf].getData()
                    firstFlag = False
                else:
                    X_aux, ids_aux = sessionClusteringsD[cf].getData()
                    if X_aux is not None :
                        for i,k in enumerate(ids):
                            X[i].extend(X_aux[i])
        return X, ids
