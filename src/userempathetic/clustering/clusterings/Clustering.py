"""
Jerarquía de clases abstractas que definen formas de realizar Clustering.
"""


class Clustering:
    """
    Clase abstracta que representa una forma de realizar clustering de usuarios o sesiones.
    """
    def __init__(self):
        pass

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
