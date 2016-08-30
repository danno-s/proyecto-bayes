# -*- coding: utf-8 -*-

"""
Jerarquia de clases abstractas que definen formas de realizar Clustering.
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from src.clusterClass.Cluster import Cluster
from src.clusterClass.OutliersGroup import OutliersGroup


class Clustering:
    """
    Clase abstracta que representa una forma de realizar clustering de usuarios
    o sesiones.
    """
    __metaclass__ = ABCMeta

    def __init__(self, confD=None):
        # Diccionario segun etiqueta de los clusters obtenidos y sus elementos.
        self.clustersD = dict()
        self.confD = confD or None
        self.n_outliers = None
        self.outliers = None
        self.n_clusters = 0  # Numero de clusters obtenidos.
        self.clusteringAlgorithm = self.initClusteringAlgorithm()
        try:
            self.X, self.ids = self.getData()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("No se pudieron obtener datos para realizar " +
                  str(self.__class__.__name__))
            self.X, self.ids = None, None
        # Dimension of feature vector.
        self.featuresDIM = self.__getDimension()

    def clusterize(self):
        """
        Utiliza el algoritmo de clustering DBSCAN sobre los datos para
        encontrar clusters. Los resultados quedan almacenados en la instancia
        del Clustering que ejecute esta funcion.

        Returns
        -------

        """
        # Compute DBSCAN
        if self.X is None:
            raise Exception  # TODO: Crear excepcion para esto.

        self.clusteringAlgorithm.fit(self.X)    # realizar clustering.

        # inicializar mascara de core samples.
        core_samples_mask = np.zeros_like(
            self.clusteringAlgorithm.labels_, dtype=bool)

        # mascara es True para indices de core samples
        core_samples_mask[self.clusteringAlgorithm.core_sample_indices_] = True
        unique_labels = set(self.clusteringAlgorithm.labels_)
        self.n_outliers = sum(
            [1 for x in self.clusteringAlgorithm.labels_ if x == -1])
        for k in unique_labels:

            # mascara de miembros de clase k.
            class_member_mask = (self.clusteringAlgorithm.labels_ == k)

            # Solo core sample de esa clase.
            xy = [(x, cl_id) for x, cl_id, i, j in zip(
                self.X, self.ids, class_member_mask, core_samples_mask) if i & j]
            if k != -1:
                self.clustersD[k] = Cluster(vectors=[j[0] for j in xy], ids=[
                                            j[1] for j in xy],  label=k, clusteringType=self.__class__.__name__[:-10])
            else:
                # if xy:
                #   self.clustersD[k]=Cluster(elements=xy,label=k,clusteringType=SessionLRSBelongingClustering)
                pass
        outliers_mask = (self.clusteringAlgorithm.labels_ == -1)
        x_outliers = [(x, cl_id) for x, cl_id, i in zip(
            self.X, self.ids, outliers_mask) if i]
        self.outliers = OutliersGroup(vectors=[j[0] for j in x_outliers], ids=[
                                      j[1] for j in x_outliers], clusteringType=self.__class__.__name__[:-10])
        print(self.outliers)
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

    def getOutliers(self):
        """ Retorna un Cluster que corresponde a un grupo con todos los outliers.

        Returns
        -------
        Cluster:
            Grupo con todos los outliers. No es un cluster real.

        """
        return self.outliers

    def getNumberOfClusters(self):
        return self.n_clusters

    @abstractmethod
    def initClusteringAlgorithm(self): pass

    @abstractmethod
    def getData(self): pass

    def __getDimension(self):
        """Entrega la dimension del vector de caracteristicas utilizado en el clustering.

        Returns
        -------
        int
            Numero de dimensiones de los vectores de caracteristicas. 0 si no se pudieron cargar los vectores.
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

    def __init__(self, confD=None):
        Clustering.__init__(self, confD=confD)

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

    def __init__(self, confD=None):
        Clustering.__init__(self, confD)

    @abstractmethod
    def initClusteringAlgorithm(self): pass

    @abstractmethod
    def getData(self): pass

    @abstractmethod
    def __getDimension(self): pass
