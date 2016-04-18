"""
Jerarquía de clases abstractas que definen formas de comparar sesiones o nodos.
"""
from abc import ABCMeta, abstractmethod


class Metric:
    """
    Clase abstracta Metric, representa métrica para comparar sesiones, nodos o micronodos

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare(self, comparator): pass


class SessionMetric(Metric):
    """
    Implementación de Metric específica para sesiones.
    """

    def __init__(self):
        Metric.__init__(self)

    def compare(self, comparator):
        """Compara elementos almacenados en el comparator.

        Parameters
        ----------
        comparator : SessionComparator
            un comparador de sesiones.

        Returns
        -------
        float
            distancia entre sesiones dependiendo de la métrica específica.
        """
        try:
            return self.distance(comparator.s1, comparator.s2)
        except Exception:
            return None

    @abstractmethod
    def distance(self, s1, s2): pass


class NodeMetric(Metric):
    """
    Implementación de Metric específica para nodos.
    """

    def __init__(self):
        Metric.__init__(self)

    def compare(self, comparator):
        """Compara elementos almacenados en el comparator.

        Parameters
        ----------
        comparator : NodeComparator
            un comparador de nodos.

        Returns
        -------
        float
            distancia entre nodos dependiendo de la métrica específica.
        """
        return self.distance(comparator.n1, comparator.n2)

    @abstractmethod
    def distance(self, n1, n2): pass


class UserMetric(Metric):
    """
    Implementación de Metric específica para usuarios.
    """

    def __init__(self):
        Metric.__init__(self)

    def compare(self, comparator):
        """Compara elementos almacenados en el comparator.

        Parameters
        ----------
        comparator : UserComparator
            un comparador de usuarios.

        Returns
        -------
        float
            distancia entre usuarios dependiendo de la métrica específica.
        """
        return self.distance(comparator.u1, comparator.u2)

    @abstractmethod
    def distance(self, u1, u2): pass
