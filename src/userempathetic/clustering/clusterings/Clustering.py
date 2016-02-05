"""
Clase Clustering

Clase abstracta (...)
"""

class Clustering:
    def __init__(self):
        pass

    def getCentroid(self,cluster):
        """
        Retorna los centros del cluster

        Parameters
        ----------
        cluster : Clustering
            El cluster que se quiere analizar

        Returns
        -------
        List
            Lista con los centros del cluster
        """
        N = len(cluster[0])
        return [sum([value[x]/len(cluster) for value in cluster]) for x in range(N)]

    def getMax(self,cluster):
        """
        ???
        Parameters
        ----------
        cluster : Cluster
            El cluster que se quiere analizar

        Returns
        -------
        List

        """
        N = len(cluster[0])
        return [max([value[x] for value in cluster]) for x in range(N)]

    def getMin(self,cluster):
        """
        ???
        Parameters
        ----------
        cluster : Cluster
            El cluster que se quiere analizar

        Returns
        -------
        List
        """
        N = len(cluster[0])
        return [min([value[x] for value in cluster]) for x in range(N)]


class SessionClustering(Clustering):
    pass


class UserClustering(Clustering):
    pass