# -*- coding: utf-8 -*-
from src.dataParsing.DataParser import DataParser


class Cluster:
    """
    Clase que representa un cluster, con sus elementos contenidos y etiqueta
    respectiva.
    """

    def __init__(self, vectors, ids, label, clusteringType=None, center=None):
        """
        Constructor

        Parameters
        ----------
        vectors : [float]
            lista representando los vectores de caracteristicas de los
            elementos inliers del cluster..
        ids: [int]
            lista de ids de usuario o sesion, dependiendo del clustering
            utilizado, en el mismo orden que vectors.
        label : str
            etiqueta con numero del cluster respecto del clustering realizado.
        clusteringType : str
            tipo de cluster
        -------

        """
        self.label = label
        self.vectors = vectors    # vectores de caracteristicas
        self.ids = ids         # ids de miembros del cluster
        self.size = len(self.vectors)
        assert self.size > 0
        self.features_dim = len(self.vectors[0])
        #FIXME acaso vectors no era [float] ??
        self.clusteringType = clusteringType or "unnamed"
        self.center = center

    def getCentroid(self):
        """
        Retorna el vector caracteristico del centroide del cluster

        Notes
            El "centroide" de un cluster es definido como el vector de
            caracteristica obtenido al promediar cada una de las dimensiones de
            los vectores de caracteristicas de todos los inliers del cluster.

        Returns
        -------
        [float] | [int]
            vector caracteristico del centroide del cluster
        """
        return [sum([value[x] / self.size \
                for value in self.vectors]) for x in range(self.features_dim)]

    def getMax(self):
        """
        Retorna el vector caracteristico del maximo del cluster

        Notes
            El "maximo" de un cluster es definido como el vector de
            caracteristica obtenido al obtener el maximo en cada una de las
            dimensiones de los vectores de caracteristicas de todos los inliers
            del cluster.

        Returns
        -------
        [float] | [int]
            vector caracteristico del maximo del cluster
        """
        return [max([value[x] for value in self.vectors]) \
                for x in range(self.features_dim)]

    def getMin(self):
        """
        Retorna el vector caracteristico del minimo del cluster

        Notes
            El "minimo" de un cluster es definido como el vector de
            caracteristica obtenido al obtener el minimo en cada una de las
            dimensiones de los vectores de caracteristicas de todos los inliers
            del cluster.

        Returns
        -------
        [float] | [int]
            vector caracteristico del minimo del cluster
        """
        return [min([value[x] for value in self.vectors]) \
                for x in range(self.features_dim)]

    def getVar(self):
        """
        Retorna un vector con la varianza de cada una de las
        dimensiones del cluster.
        """
        mean = self.getCentroid()
        return [sum([(value[x] - mean[x]) ** 2 / self.size \
                for value in self.vectors]) \
                for x in range(self.features_dim)]

    def __str__(self):
        return self.clusteringType + ":\n" +\
                "Cluster " + \
                str(self.label) + \
                ",\t#" + \
                str(self.size) + \
                " inliers"  \
                "\n Members IDs:\n\t" + \
                str(self.ids) + \
                "\n Representative Member(s):\n\t" + \
                str(self.getRepresentativeMember())
        #"\n Elements Features:\n\t" + str(self.elements) + \

    def toSQLItem(self):
        """
        Retorna tupla de strings con representacion de los items que se
        almacenan en la base de datos SQL para el Cluster.

        Returns
        -------
        (str,str,str,str,str)
            Tupla de str definida por (label,ids,centroide,clusteringType,
            vectores)
        """
        return str(self.label), \
                ' '.join([str(x) for x in self.ids]), \
                ' '.join([str(x) for x in self.getCentroid()]), \
                self.clusteringType, \
                ';'.join([' '.join(map(str, x)) for x in self.vectors])

    def getRepresentativeMember(self):
        """
        Retorna str que muestra informacion del miembro(s) representativo(s)
        del cluster.

        Returns
        -------
        str:
            Informacion del miembro representativo del cluster.
        """
        if self.clusteringType == 'UMSBCKMeans' and self.center is not None:
            return self.center
        elif 'User' in self.clusteringType and \
                self.clusteringType != 'SessionUserClustersBelonging':
            return self.__getRepresentativeUser()
        elif 'Session' in self.clusteringType:
            return self.__getRepresentativeSession()
        else:
            print("Failed")

    def __getRepresentativeUser(self):
        centroid_vector = self.getCentroid()
        closestU = []
        closestV = set()
        min_dist = 100.
        from scipy.spatial.distance import cityblock
        for x, u_id in zip(self.vectors, self.ids):
            d = cityblock(x, centroid_vector)
            if d == min_dist:
                closestU.append(u_id)
                closestV.add(str(x))
            elif d < min_dist:
                closestU.clear()
                closestV.clear()
                closestU.append(u_id)
                closestV.add(str(x))
                min_dist = d

        s = "Centroid: " + str(centroid_vector) + "\n\t"
        s += "Min Distance to centroid: " + str(min_dist) + "\n\t"
        s += "Closest User(s) with profiles: "
        for u in closestU:
            s += str(u) + " [" + DataParser().getProfileOf(u) + "], \t"
        s += "\n\tClosest Vector(s): \n\t"
        for v in closestV:
            s += str(v) + "\n\t"
        return s

    def __getRepresentativeSession(self):
        from src.utils.comparatorUtils import getSession
        centroid_vector = self.getCentroid()
        closestS = []
        closestV = set()
        min_dist = 100.
        from scipy.spatial.distance import cityblock
        for x, s_id in zip(self.vectors, self.ids):
            d = cityblock(x, centroid_vector)
            if d == min_dist:
                closestS.append(s_id)
                closestV.add(str(x))
            elif d < min_dist:
                closestS.clear()
                closestV.clear()
                closestS.append(s_id)
                closestV.add(str(x))
                min_dist = d

        s = "Centroid: " + str(centroid_vector) + "\n\t"
        s += "Min Distance to centroid: " + str(min_dist) + "\n\t"
        s += "Closest Session(s) with profiles: \n\t"
        for s_id in closestS:
            s += str(getSession(s_id)) + "\n\t"
        s += "\n\tClosest Vector(s): \n\t"
        for v in closestV:
            s += str(v) + "\n\t"
        return s