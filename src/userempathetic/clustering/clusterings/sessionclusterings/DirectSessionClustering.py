from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.clusterClass.Cluster import Cluster
from src.userempathetic.sessionComparator.SessionComparator import SessionComparator
from src.userempathetic.metrics.sessionMetrics.NodeMetrics import SequenceMSSDistance
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs

class DirectSessionClustering(SessionClustering):
    """
    Clase DirectSessionClustering implementa un SessionClustering que realiza clustering utilizando
    todos los features de sesiones, concatenados en un mismo vector.
    """

    tablename = 'sessionclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid,clustering_name) VALUES (%s,%s,%s,%s)'
    xlabel = "IDs de Sesiones"
    ylabel = "Distancia"
    title = "Distancia a otras sesiones, para sesión representativa de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=1.0, min_samples=5, metric='precomputed') # X is distance matrix.

    @classmethod
    def getData(self):
        ids = getAllSessionIDs()
        N = len(ids)
        import itertools
        s_pairs = itertools.combinations_with_replacement(ids,2)
        X = np.zeros([N, N], dtype= np.float64)
        for sp in s_pairs:
            sC = SessionComparator(sp[0],sp[1])
            X[sp[0]-1,sp[1]-1] = sC.compareSessions(SequenceMSSDistance())
            X[sp[1]-1,sp[0]-1] = X[sp[0]-1,sp[1]-1]
        return X,ids


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


if __name__ == '__main__':
    dsc = DirectSessionClustering()
