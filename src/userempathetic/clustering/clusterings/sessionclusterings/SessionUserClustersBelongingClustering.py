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

    tablename = 'sessionclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid,clustering_name) VALUES (%s,%s,%s,%s)'
    xlabel = "User Cluster IDs"
    ylabel = "Pertenencia del usuario-cluster"
    title = "Pertenencia de usuario-cluster por sesión representativa de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=0.8, min_samples=5, metric='manhattan')

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

    def __getDimension(self):
        """Entrega la dimensión del vector de características utilizado en el clustering.

        Returns
        -------
        int
            Numero de dimensiones de los vectores de características.
        """
        if self.X is None:
            return 0
        return len(self.X[0])
