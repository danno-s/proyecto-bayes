
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
        # TODO: VERIFICAR parámetro ELEMENTS
        self.label = label
        self.elements = [x[0] for x in elements]    # vectores de características
        self.ids = [x[1] for x in elements]         # ids de elementos
        self.size = len(self.elements)
        assert self.size > 0
        self.features_dim = len(self.elements[0])
        self.clusteringType = clusteringType or ""

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
                                                                        "\n Elements IDs:\n\t" + str(self.ids) + \
               "\n Elements Features:\n\t" + str(self.elements)

    def toSQLItem(self):
        return str(self.label), ' '.join([str(x) for x in self.ids]), ' '.join([str(x) for x in self.getCentroid()]), self.clusteringType.__name__[:-10]
