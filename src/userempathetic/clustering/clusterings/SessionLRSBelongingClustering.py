from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.clusterClass.Cluster import Cluster


class SessionLRSBelongingClustering(SessionClustering):
    """Clase SessionLRSBelongingClustering implementa un SessionClustering que realiza clustering utilizando
    el feature LRSBelongingFeature.

    See Also
        LRSBelongingFeature
    """

    tablename = 'sessionlrsbelongingclusters'
    sqlWrite = 'INSERT INTO ' + tablename + ' (cluster_id,members,centroid) VALUES (%s,%s,%s)'
    xlabel = "LRSs IDs"
    ylabel = "Utilización del LRS"
    title = "Uso de LRSs por sesión representativa de cada cluster"

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        SessionClustering.__init__(self)
        self.clusteringAlgorithm = DBSCAN(eps=0.5, min_samples=5, metric='manhattan')
        self.X, self.ids = self.__getData()
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
        for k in unique_labels:
            class_member_mask = (self.clusteringAlgorithm.labels_ == k)
            xy = [(x, id) for x, id, i, j in zip(self.X, self.ids, class_member_mask, core_samples_mask) if i & j]
            if k != -1:
                self.clustersD[k] = Cluster(elements=xy, label=k, clusteringType=SessionLRSBelongingClustering)
            else:
                print("# outliers = "+ str(len(xy)))
                # if xy:
                #   self.clustersD[k]=Cluster(elements=xy,label=k,clusteringType=SessionLRSBelongingClustering)
                pass
        # Number of clusters in labels, ignoring noise if present.
        self.n_clusters = len(unique_labels)
        if -1 in self.clusteringAlgorithm.labels_:
            self.n_clusters -= 1

    def __getData(self):
        sqlFT = sqlWrapper(db='FT')
        sqlRead = 'select session_id,vector from sessionlrsbelongingfeatures'
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
        if self.X == None:
            return 0
        return len(self.X[0])