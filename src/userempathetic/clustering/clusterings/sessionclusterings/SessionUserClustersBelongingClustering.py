from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.clusterClass.Cluster import Cluster


class SessionUserClustersBelongingClustering(SessionClustering):
    """Clase SessionUserClustersBelongingClustering implementa un SessionClustering que realiza clustering utilizando
    el feature UserClustersBelongingFeature.

    See Also
        UserClustersBelongingFeature
    """
    xlabel = "User Cluster IDs"
    ylabel = "Pertenencia del usuario-cluster"
    title = "Pertenencia de usuario-cluster por sesión representativa de cada cluster"

    def __init__(self,confD=None):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self,confD=confD)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=self.confD['eps'], min_samples=self.confD['min_samples'], metric=self.confD['metric'])

    @classmethod
    def getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select session_id,vector from sessionfeatures where feature_name = '+"'SessionUserClustersBelonging'"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            if row[1] is None:
                raise Exception #TODO: Crear excepción para esto
            vector = row[1].split(' ')
            for x in vector:
                if x == '':
                    raise Exception #TODO: Crear excepción para esto
            ids.append(int(row[0]))
            X.append([int(x) for x in vector])
        return X, ids
