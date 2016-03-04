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
        self.clusteringAlgorithm = DBSCAN(eps=1.0, min_samples=1, metric='precomputed') # X is distance matrix.
        self.X, self.ids = self.getData()
        self.featuresDIM = self.__getDimension()  # Dimension of feature vector.

    def clusterize(self):
        """Utiliza el algoritmo de clustering DBSCAN sobre los datos para encontrar clusters. Los resultados
        quedan almacenados en la instancia del Clustering que ejecute esta función.

        Returns
        -------

        """
        # Compute DBSCAN
        self.clusteringAlgorithm.fit(self.X)
        core_samples_mask = np.zeros_like(self.clusteringAlgorithm.labels_, dtype=bool)
        core_samples_mask[self.clusteringAlgorithm.core_sample_indices_] = True
        unique_labels = set(self.clusteringAlgorithm.labels_)
        self.n_outliers = sum([1 for x in self.clusteringAlgorithm.labels_ if x == -1])
        print("# outliers = %d" % self.n_outliers)
        for k in unique_labels:
            class_member_mask = (self.clusteringAlgorithm.labels_ == k)
            xy = [(x, cl_id) for x, cl_id, i, j in zip(self.X, self.ids, class_member_mask, core_samples_mask) if i & j]
            if k != -1:
                self.clustersD[k] = Cluster(elements=xy, label=k, clusteringType=DirectSessionClustering)
            else:
                # if xy:
                #   self.clustersD[k]=Cluster(elements=xy,label=k,clusteringType=SessionLRSBelongingClustering)
                pass
        # Number of clusters in labels, ignoring noise if present.
        self.n_clusters = len(unique_labels)
        if -1 in self.clusteringAlgorithm.labels_:
            self.n_clusters -= 1

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
