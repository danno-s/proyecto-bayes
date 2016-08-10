# -*- coding: utf-8 -*-

from src.clusterClass.Cluster import Cluster


class OutliersGroup(Cluster):
    """ Define un grupo de elementos clasificados como Outliers por el algoritmo de clustering.
    Se implementa como un Cluster debido a que permite guardar con un formato similar al del Cluster
    en la base de datos los outliers obtenidos en cada clustering utilizando el label "-1".

    """

    def __init__(self, vectors, ids, clusteringType=None):
        Cluster.__init__(self, vectors, ids, -1, clusteringType)

    def toSQLItem(self):
        """ Retorna version reducida del SQL string, asignando None a la columna del centroide.

        Returns
        -------
        (str,str,None,str,str)
        """
        return self.label, ' '.join([str(x) for x in self.ids]), None, self.clusteringType, ';'.join([' '.join(map(str, x)) for x in self.vectors])

    def getCentroid(self):
        return None

    def getMax(self):
        return None

    def getMin(self):
        return None

    def getRepresentativeMember(self):
        return None

    def __str__(self):
        return "Group of Outliers:" + "\t#" + str(self.size) + " outliers \n Outliers IDs:\n\t" + str(self.ids) + "\n"
