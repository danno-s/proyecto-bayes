"""
Jerarquía de clases abstractas que definen formas de realizar Clustering.
"""
from abc import ABCMeta, abstractmethod


class Clustering:
    """
    Clase abstracta que representa una forma de realizar clustering de usuarios o sesiones.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.clustersD = dict()  # Diccionario según etiqueta de los clusters obtenidos y sus elementos.
        self.n_outliers = None
        self.n_clusters = 0  # Número de clusters obtenidos.


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

class SessionClustering(Clustering):
    """
    Clase abstracta Clustering, representa una forma de realizar clustering de sesiones.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Clustering.__init__(self)


class UserClustering(Clustering):
    """
    Clase abstracta Clustering, representa una forma de realizar clustering de usuarios.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Clustering.__init__(self)

