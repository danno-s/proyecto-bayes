"""
Definición de distintas Distance (implementacicones de UserMetric) que utilizan los Features extraídos de usuarios.
"""
from src.userempathetic.metrics.Metric import UserMetric
from src.userempathetic.utils.comparatorUtils import getFeatureOfUser


class UserLRSHistogramDistance(UserMetric):
    """
    Clase que implementa la métrica como una distancia entre los vectores histograma de LRS (LRS Histogram).
    """
    def __init__(self):
        UserMetric.__init__(self)

    def distance(self, u1, u2):
        """Distancia de las usuarios s1 y s2 definida como la suma del valor absoluto de las diferencias
         elemento a elemento de los vectores histograma de LRS (LRS Histogram).

        Parameters
        ----------
        u1 : int
            un id de usuario.
        u2 : int
            un id de usuario.
        Returns
        -------
        float
            distancia calculada.
        """
        v1 = self.getLRSHistogramVector(u1)
        v2 = self.getLRSHistogramVector(u2)
        print(v1)
        print(v2)
        return float(sum([abs(x - y) for x, y in zip(v1, v2)]))

    def getLRSHistogramVector(self, user_id):
        """Retorna vector histograma de LRS (LRS Histogram) del usuario indicado.

        Parameters
        ----------
        user_id : int
            id de usuario

        Returns
        -------
        [int]
            vector de histograma de LRS (LRS Histogram) del usuario.
        """
        return getFeatureOfUser(user_id, 'UserLRSHistogram')

class UserURLsBelongingDistance(UserMetric):
    """
    Clase que implementa la métrica como una distancia entre los vectores de pertenencia a URLs (URLs Belonging vector).
    """
    def __init__(self):
        UserMetric.__init__(self)

    def distance(self, u1, u2):
        """Distancia de las usuarios s1 y s2 definida como la suma del valor absoluto de las diferencias
         elemento a elemento de los vectores de pertenencia a URLs (URLs Belonging vectors).

        Parameters
        ----------
        u1 : int
            un id de usuario.
        u2 : int
            un id de usuario.
        Returns
        -------
        float
            distancia calculada.
        """
        v1 = self.getURLsBelongingVector(u1)
        v2 = self.getURLsBelongingVector(u2)
        print(v1)
        print(v2)
        return float(sum([abs(x - y) for x, y in zip(v1, v2)]))

    def getURLsBelongingVector(self, user_id):
        """Retorna vector de pertenencia a URLs (URLs Belonging vector) del usuario indicado.

        Parameters
        ----------
        user_id : int
            id de usuario

        Returns
        -------
        [int]
            vector de pertenencia a URLs (URLs Belonging vector) del usuario.
        """
        return getFeatureOfUser(user_id, 'UserURLsBelonging')
