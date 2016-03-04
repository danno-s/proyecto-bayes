from src.userempathetic.clustering.clusterings.Clustering import UserClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.clusterClass.Cluster import Cluster


class UserURLsBelongingClustering(UserClustering):
    """Clase UserURLsBelongingClustering implementa un UserClustering que realiza clustering utilizando
    el feature UserURLsBelongingFeature.

    See Also
        UserURLsBelongingFeature
    """
    tablename = 'userclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid,clustering_name) VALUES (%s,%s,%s,%s)'
    xlabel = "URLs IDs"
    ylabel = "Utilización de URLs"
    title = "Uso de URLs por usuario representativo de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        UserClustering.__init__(self)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=1.0, min_samples=5, metric='euclidean')  # TODO: Configurar parámetros desde archivo de config.

    @classmethod
    def getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select user_id,vector from userfeatures where feature_name = '+"'UserURLsBelonging'"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([int(x) for x in row[1].split(' ')])
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
