
from abc import ABCMeta, abstractmethod
from scipy.spatial import distance

class Metrics:

    __metaclass__ = ABCMeta

    @abstractmethod
    def metSession(self, session):  pass

    @abstractmethod
    def metNode(self, node):  pass

    @abstractmethod
    def metMicro(self, micro): pass

class Euclidean(Metrics):

    def metSession(self, session):
