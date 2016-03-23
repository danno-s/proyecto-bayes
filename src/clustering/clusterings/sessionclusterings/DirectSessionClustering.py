from src.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.clusterClass.Cluster import Cluster
from src.sessionComparator.SessionComparator import SessionComparator
from src.metrics.sessionMetrics.DirectMetrics import SequenceMSSDistance
from src.utils.featureExtractionUtils import getAllSessionIDs
from src.utils.sqlUtils import sqlWrapper

class DirectSessionClustering(SessionClustering):
    """
    Clase DirectSessionClustering implementa un SessionClustering que realiza clustering utilizando
    todos los features de sesiones, concatenados en un mismo vector.
    """

    xlabel = "IDs de Sesiones"
    ylabel = "Distancia"
    title = "Distancia a otras sesiones, para sesión representativa de cada cluster"

    def __init__(self,confD=None):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self,confD=confD)

    def initClusteringAlgorithm(self):
        return DBSCAN(eps=self.confD['eps'], min_samples=self.confD['min_samples'], metric=self.confD['metric']) # X is distance matrix.

    @classmethod
    def getData(self):

        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select session_id,vector from sessionfeatures where feature_name = '+"'SessionDistance'"
        rows = sqlFT.read(sqlRead)
        assert len(rows) > 0
        vectors = list()
        ids = list()
        for row in rows:
            ids.append(int(row[0]))
            vectors.append([float(x) for x in row[1].split(' ')])
        N = len(ids)
        X = np.zeros([N, N], dtype=np.float64)
        for i,vec in enumerate(vectors):
            for k,v in enumerate(vec):
                X[i,k] = v
        return X, ids
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
        #TODO: guardar en DB el feature de "distancia"
        return X,ids
        '''

if __name__ == '__main__':
    dsc = DirectSessionClustering()
