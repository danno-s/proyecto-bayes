"""
Clase abstracta Metrics, representa métricas para comparar sesiones, nodos o micronodos
"""
from abc import ABCMeta, abstractmethod
from scipy.spatial import distance


class Metrics:
    __metaclass__ = ABCMeta

    @abstractmethod
    def metSession(self, session): pass

    @abstractmethod
    def metNode(self, node): pass

    @abstractmethod
    def metMicro(self, micro): pass


class Euclidean(Metrics):
    def __init__(self):
        self.L = list()
        self.p = None

    def metSession(self, session):
        node = session.getFirstNode()
        while node.next:
            node.accept(self)
            node = node.next

    def metNode(self, node):
        node.microNode.accept(self)

    def metMicro(self, micro):
        if not self.p:
            pass
        else:
            self.L.extend(distance.euclidean(self.p, micro.toList()))
        self.p = micro.toList()
