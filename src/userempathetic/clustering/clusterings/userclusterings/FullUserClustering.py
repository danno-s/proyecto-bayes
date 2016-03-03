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
    tablename = 'fulluserclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid) VALUES (%s,%s,%s)'
    xlabel = "Dimensiones"
    ylabel = "Valor"
    title = "Valores en cada dimensión de usuario representativo de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        UserClustering.__init__(self)
        self.clusteringAlgorithm = DBSCAN(eps=1.0, min_samples=15,
                                          metric='manhattan')  # TODO: Configurar parámetros desde archivo de config.
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
                self.clustersD[k] = Cluster(elements=xy, label=k, clusteringType=self.__name__)
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
        X_lrs, ids = UserLRSHistogramClustering.getData()
        X_url, _ = UserURLsBelongingClustering.getData()
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

if __name__ == '__main__':
    fuc = FullUserClustering()
    print(fuc.featuresDIM)
    print(UserLRSHistogramClustering().featuresDIM)
    print(UserURLsBelongingClustering().featuresDIM)