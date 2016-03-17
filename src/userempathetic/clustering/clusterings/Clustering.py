"""
Jerarquía de clases abstractas que definen formas de realizar Clustering.
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from src.userempathetic.clusterClass.Cluster import Cluster


class Clustering:
    """
    Clase abstracta que representa una forma de realizar clustering de usuarios o sesiones.
    """
    __metaclass__ = ABCMeta

    def __init__(self,confD=None):
        self.clustersD = dict()  # Diccionario según etiqueta de los clusters obtenidos y sus elementos.
        self.confD = confD or None
        self.n_outliers = None
        self.n_clusters = 0  # Número de clusters obtenidos.
        self.clusteringAlgorithm = self.initClusteringAlgorithm()
        try:
            self.X, self.ids = self.getData()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("No se pudieron obtener datos para realizar "+ str(self.__class__.__name__))
            self.X, self.ids = None, None
        self.featuresDIM = self.__getDimension()  # Dimension of feature vector.

    def clusterize(self):
        """Utiliza el algoritmo de clustering DBSCAN sobre los datos para encontrar clusters. Los resultados
        quedan almacenados en la instancia del Clustering que ejecute esta función.

        Returns
        -------

        """
        # Compute DBSCAN
        if self.X is None:
            raise Exception #TODO: Crear excepcion para esto.
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
                self.clustersD[k] = Cluster(vectors=[j[0] for j in xy],ids=[j[1] for j in xy],  label=k, clusteringType=self.__class__.__name__[:-10])
            else:
                # if xy:
                #   self.clustersD[k]=Cluster(elements=xy,label=k,clusteringType=SessionLRSBelongingClustering)
                pass
        # Number of clusters in labels, ignoring noise if present.
        self.n_clusters = len(unique_labels)
        if -1 in self.clusteringAlgorithm.labels_:
            self.n_clusters -= 1


    def getClusters(self):
        """Retorna diccionario con los clusters extraidos.

        Returns
        -------
        dict
            diccionario con los clusters extraidos.
        """
        return self.clustersD

    def getNumberOfClusters(self):
        return self.n_clusters

    @abstractmethod
    def initClusteringAlgorithm(self): pass

    @abstractmethod
    def getData(self): pass

    def __getDimension(self):
        """Entrega la dimensión del vector de características utilizado en el clustering.

        Returns
        -------
        int
            Numero de dimensiones de los vectores de características. 0 si no se pudieron cargar los vectores.
        """
        if self.X is None:
            return 0
        return len(self.X[0])

    def getSQLWrite(self):
        return 'INSERT INTO ' + self.tablename + ' (cluster_id,members,centroid,clustering_name,vectors) VALUES (%s,%s,%s,%s,%s)'


class SessionClustering(Clustering):
    """
    Clase abstracta Clustering, representa una forma de realizar clustering de sesiones.
    """
    __metaclass__ = ABCMeta
    tablename = 'sessionclusters'

    def __init__(self,confD=None):
        Clustering.__init__(self,confD=confD)

    @abstractmethod
    def initClusteringAlgorithm(self): pass

    @abstractmethod
    def getData(self): pass

    @abstractmethod
    def __getDimension(self): pass


class UserClustering(Clustering):
    """
    Clase abstracta Clustering, representa una forma de realizar clustering de usuarios.
    """
    __metaclass__ = ABCMeta
    tablename = 'userclusters'

    def __init__(self,confD=None):
        Clustering.__init__(self,confD)

    @abstractmethod
    def initClusteringAlgorithm(self): pass

    @abstractmethod
    def getData(self): pass

    @abstractmethod
    def __getDimension(self): pass
