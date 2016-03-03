from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.clusterClass.Cluster import Cluster
from src.userempathetic.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import SessionUserClustersBelongingClustering
from src.userempathetic.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering

class FullSessionClustering(SessionClustering):
    """
    Clase FullSessionClustering implementa un SessionClustering que realiza clustering utilizando
    todos los features de sesiones, concatenados en un mismo vector.
    """

    tablename = 'fullsessionclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid) VALUES (%s,%s,%s)'
    xlabel = "Dimensiones"
    ylabel = "Valor"
    title = "Valores en cada dimensión de sesión representativa de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self)
        self.clusteringAlgorithm = DBSCAN(eps=2.5, min_samples=15, metric='euclidean')
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
        n_outliers = sum([1 for x in self.clusteringAlgorithm.labels_ if x == -1])
        print("# outliers = %d" % n_outliers)
        for k in unique_labels:
            class_member_mask = (self.clusteringAlgorithm.labels_ == k)
            xy = [(x, cl_id) for x, cl_id, i, j in zip(self.X, self.ids, class_member_mask, core_samples_mask) if i & j]
            if k != -1:
                self.clustersD[k] = Cluster(elements=xy, label=k, clusteringType=FullSessionClustering)
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
        X_lrs, ids = SessionLRSBelongingClustering.getData()
        X_url, _ = SessionUserClustersBelongingClustering.getData()
        X = list()
        for i,user_id in enumerate(ids):
            vector = X_lrs[i]
            vector.extend(X_url[i])
            X.append(vector)

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
