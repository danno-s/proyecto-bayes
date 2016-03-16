

class Cluster:
    """
    Clase que representa un cluster, con sus elementos contenidos y etiqueta respectiva.
    """
    def __init__(self, elements, label, clusteringType=None):
        """Constructor

        Parameters
        ----------
        elements : ([float],[int])
            tupla representando los elementos inliers del cluster de la forma ([vector],[id]).
            Las ids pueden ser de usuario o sesión, dependiendo del clustering utilizado.
        label : str
            etiqueta con número del cluster respecto del clustering realizado.
        clusteringType : str
            tipo de cluster
        -------

        """
        self.label = label
        self.elements = [x[0] for x in elements]    # vectores de características
        self.ids = [x[1] for x in elements]         # ids de miembros del cluster
        self.size = len(self.elements)
        assert self.size > 0
        self.features_dim = len(self.elements[0])
        self.clusteringType = clusteringType[:-10] or "unnamed"

    def getCentroid(self):
        """Retorna el vector característico del centroide del cluster

        Notes
            El "centroide" de un cluster es definido como el vector de característica obtenido al promediar cada una de
            las dimensiones de los vectores de características de todos los inliers del cluster.

        Returns
        -------
        [float] | [int]
            vector característico del centroide del cluster
        """
        return [sum([value[x] / self.size for value in self.elements]) for x in range(self.features_dim)]

    def getMax(self):
        """Retorna el vector característico del máximo del cluster

        Notes
            El "máximo" de un cluster es definido como el vector de característica obtenido al obtener el
            máximo en cada una de las dimensiones de los vectores de características de todos los inliers del cluster.

        Returns
        -------
        [float] | [int]
            vector característico del máximo del cluster
        """
        return [max([value[x] for value in self.elements]) for x in range(self.features_dim)]

    def getMin(self):
        """Retorna el vector característico del mínimo del cluster

        Notes
            El "mínimo" de un cluster es definido como el vector de característica obtenido al obtener el
            mínimo en cada una de las dimensiones de los vectores de características de todos los inliers del cluster.

        Returns
        -------
        [float] | [int]
            vector característico del mínimo del cluster
        """
        return [min([value[x] for value in self.elements]) for x in range(self.features_dim)]

    def __str__(self):

        return "Cluster " + str(self.label) + ",\t#" + str(self.size) + " inliers" \
                                                                        "\n Members IDs:\n\t" + str(self.ids) + \
                "\n Representative Member(s):\n\t" + str(self.getRepresentativeMember())
               #"\n Elements Features:\n\t" + str(self.elements) + \


    def toSQLItem(self):
        return str(self.label), ' '.join([str(x) for x in self.ids]), ' '.join([str(x) for x in self.getCentroid()]), \
               self.clusteringType

    def getRepresentativeMember(self):
        if 'User' in self.clusteringType and self.clusteringType != 'SessionUserClustersBelonging':
            return self.getRepresentativeUser()
        elif 'Session' in self.clusteringType:
            return self.getRepresentativeSession()
        else:
            print("Failed")

    def getRepresentativeUser(self):
        from src.userempathetic.utils.dataParsingUtils import getProfileOf
        centroid_vector = self.getCentroid()
        closestU = []
        closestV = set()
        min_dist = 100.
        from scipy.spatial.distance import cityblock
        for x,u_id in zip(self.elements,self.ids):
            d = cityblock(x,centroid_vector)
            if d == min_dist:
                closestU.append(u_id)
                closestV.add(str(x))
            elif d < min_dist:
                closestU.clear()
                closestV.clear()
                closestU.append(u_id)
                closestV.add(str(x))
                min_dist = d

        s = "Centroid: " +str(centroid_vector) + "\n\t"
        s += "Min Distance to centroid: "+ str(min_dist) + "\n\t"
        s += "Closest User(s) with profiles: "
        for u in closestU:
            s+= str(u) + " ["+ str(getProfileOf(u)) + "], \t"
        s += "\n\tClosest Vector(s): \n\t"
        for v in closestV:
            s += str(v) + "\n\t"
        return s

    def getRepresentativeSession(self):
        from src.userempathetic.utils.comparatorUtils import getSimulSession
        centroid_vector = self.getCentroid()
        closestS = []
        closestV = set()
        min_dist = 100.
        from scipy.spatial.distance import cityblock
        for x,s_id in zip(self.elements,self.ids):
            d = cityblock(x,centroid_vector)
            if d == min_dist:
                closestS.append(s_id)
                closestV.add(str(x))
            elif d < min_dist:
                closestS.clear()
                closestV.clear()
                closestS.append(s_id)
                closestV.add(str(x))
                min_dist = d

        s = "Centroid: " +str(centroid_vector) + "\n\t"
        s += "Min Distance to centroid: "+ str(min_dist) + "\n\t"
        s += "Closest Session(s) with profiles: \n\t"
        for s_id in closestS:
            s+= str(getSimulSession(s_id)) + "\n\t"
        s += "\n\tClosest Vector(s): \n\t"
        for v in closestV:
            s += str(v) + "\n\t"
        return s