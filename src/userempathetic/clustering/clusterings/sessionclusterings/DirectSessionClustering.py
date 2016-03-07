from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.clusterClass.Cluster import Cluster
from src.userempathetic.sessionComparator.SessionComparator import SessionComparator
from src.userempathetic.metrics.sessionMetrics.NodeMetrics import SequenceMSSDistance
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs
from src.userempathetic.utils.sqlUtils import sqlWrapper

class DirectSessionClustering(SessionClustering):
    """
    Clase DirectSessionClustering implementa un SessionClustering que realiza clustering utilizando
    todos los features de sesiones, concatenados en un mismo vector.
    """

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
        return DBSCAN(eps=3.0, min_samples=5, metric='precomputed') # X is distance matrix.

    @classmethod
    def getData(self):
        #TODO: Cambiar para que lea de tabla 'sessionfeatures'.
        '''
        ids = getAllSessionIDs()
        N = len(ids)
        import itertools
        s_pairs = itertools.combinations_with_replacement(ids,2)
        X = np.zeros([N, N], dtype= np.float64)
        for sp in s_pairs:
            sC = SessionComparator(sp[0],sp[1],simulation=True) #TODO: OR FALSE??
            X[sp[0]-1,sp[1]-1] = sC.compareSessions(SequenceMSSDistance())
            X[sp[1]-1,sp[0]-1] = X[sp[0]-1,sp[1]-1]
        return X,ids
        '''
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select session_id,vector from sessionfeatures where feature_name = '+"'SessionDistance'"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        X = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([float(x) for x in row[1].split(' ')])
        return X, ids


if __name__ == '__main__':
    dsc = DirectSessionClustering()
