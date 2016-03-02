"""
Jerarquía de clases abstractas que definen características (Features) de sesiones o usuarios.
"""
from abc import ABCMeta, abstractmethod


class Feature:
    """
    Clase abstracta Feature, representa una característica de un usuario o sesión.
    """
    __metaclass__ = ABCMeta

    def __init__(self, simulation=False):
        """Constructor

        Parameters
        ----------
        simulation : bool
            Si es True, el modo de cálculo de los features será basado en los datos simulados si es que existen.

        Returns
        -------

        """
        if not simulation:
            self.simulation = False
        else:
            self.simulation = True
        pass

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

    def __init__(self, simulation=False):
        Feature.__init__(self,simulation)

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

    def __init__(self, simulation=False):
        Feature.__init__(self,simulation)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def extractSimulated(self): pass

    @abstractmethod
    def toSQLItem(self): pass
