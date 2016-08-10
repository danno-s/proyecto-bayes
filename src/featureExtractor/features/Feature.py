"""
Jerarquia de clases abstractas que definen caracteristicas (Features) de sesiones o usuarios.
"""
from abc import ABCMeta, abstractmethod


class Feature:
    """
    Clase abstracta Feature, representa una caracteristica de un usuario o sesion.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def toSQLItem(self):
        pass


class UserFeature(Feature):
    """
    Implementacion abstracta especifica de Features de usuario.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Feature.__init__(self)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def toSQLItem(self): pass


class SessionFeature(Feature):
    """
    Implementacion abstracta especifica de Features de sesion.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Feature.__init__(self)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def toSQLItem(self): pass
