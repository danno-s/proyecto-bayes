"""
Clase Cluster

Representa un cluster y sus características
"""

class Cluster:

    def __init__(self, elements, label, clusteringType=None):
        """
        Constructor de la clase

        Parameters
        ----------
        elements : List
            Los elementos del cluster
        label : String
            Nombre del cluster
        clusteringType : String
            Tipo de cluster
        -------

        """
        self.label = label
        self.elements = [x[0] for x in elements]
        self.ids = [x[1] for x in elements]
        self.size = len(self.elements)
        assert self.size > 0
        self.features_dim = len(self.elements[0])
        self.clusteringType = clusteringType or ""

    def getCentroid(self):
        """
        Retorna los centros del cluster

        Returns
        -------
        List
            Lista con los centros del cluster
        """
        return [sum([value[x] / self.size for value in self.elements]) for x in range(self.features_dim)]

    def getMax(self):
        """
        ????

        Returns
        -------
        List

        """
        return [max([value[x] for value in self.elements]) for x in range(self.features_dim)]

    def getMin(self):
        """
        ????

        Returns
        -------
        List

        """
        return [min([value[x] for value in self.elements]) for x in range(self.features_dim)]


    def __str__(self):
        return "Cluster "+ str(self.label)+",\t#"+str(self.size) + " inliers"\
                                                                    "\n Elements IDs:\n"+ str(self.ids)+\
                                                                    "\n Elements Features:\n"+ str(self.elements)