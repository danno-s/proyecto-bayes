"""
Clase abstracta Metric, representa métrica para comparar sesiones, nodos o micronodos
"""
from abc import ABCMeta, abstractmethod

from src.userempathetic.sessionComparator.NodeComparator import NodeComparator


class Metric:
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare(self, comparator): pass


class SessionMetric(Metric):
    def __init__(self):
        Metric.__init__(self)

    def compare(self, comparator):
        s1 = comparator.s1
        s2 = comparator.s2
        value = self.distance(s1, s2)
        return value

    @abstractmethod
    def distance(self, s1, s2): pass


class NodeMetric(Metric):
    def __init__(self):
        Metric.__init__(self)

    def compare(self, comparator):
        n1 = comparator.n1
        n2 = comparator.n2
        value = self.distance(n1, n2)
        return value

    @abstractmethod
    def distance(self, s1, s2): pass
