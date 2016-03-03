"""
Jerarquía de clases abstractas que definen formas de realizar Clustering.
"""


class Clustering:
    """
    Clase abstracta que representa una forma de realizar clustering de usuarios o sesiones.
    """

    def __init__(self):
        self.clustersD = dict()  # Diccionario según etiqueta de los clusters obtenidos y sus elementos.
        self.n_clusters = 0  # Número de clusters obtenidos.
        pass

    def getClusters(self):
        """Retorna diccionario con los clusters extraidos.

        Returns
        -------
        dict
            diccionario con los clusters extraidos.
        """
        return self.clustersD


class SessionClustering(Clustering):
    """
    Clase abstracta Clustering, representa una forma de realizar clustering de sesiones.
    """
    pass


class UserClustering(Clustering):
    """
    Clase abstracta Clustering, representa una forma de realizar clustering de usuarios.
    """
    pass
