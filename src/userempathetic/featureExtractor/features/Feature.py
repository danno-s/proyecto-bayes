"""
Jerarquía de clases abstractas que definen características (Features) de sesiones o usuarios.
"""
from abc import ABCMeta, abstractmethod


class Feature:
    """
    Clase abstracta Feature, representa una característica de un usuario o sesión.
    """
    __metaclass__ = ABCMeta

    def __init__(self): pass

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def extractSimulated(self): pass

    @abstractmethod
    def toSQLItem(self): pass


class UserFeature(Feature):
    """
    Implementación abstracta específica de Features de usuario.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Feature.__init__(self)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def extractSimulated(self): pass

    @abstractmethod
    def toSQLItem(self): pass


class SessionFeature(Feature):
    """
    Implementación abstracta específica de Features de sesión.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Feature.__init__(self)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def extractSimulated(self): pass

    @abstractmethod
    def toSQLItem(self): pass
