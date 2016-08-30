# -*- coding: utf-8 -*-

"""
Definicion de distintas Distance (implementacicones de UserMetric) que utilizan los Features extraidos de usuarios.
"""
from src.metrics.Metric import UserMetric
from src.utils.comparatorUtils import getFeatureOfUser


class UserLRSHistogramDistance(UserMetric):
    """
    Clase que implementa la metrica como una distancia entre los vectores histograma de LRS (LRS Histogram).
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
        if v1 or v2 is None:
            raise Exception  # TODO: Crear excepcion para esto.
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


class UserMacroStatesBelongingDistance(UserMetric):
    """
    Clase que implementa la metrica como una distancia entre los vectores de pertenencia a macro_ids (macro_ids Belonging vector).
    """

    def __init__(self):
        UserMetric.__init__(self)

    def distance(self, u1, u2):
        """Distancia de las usuarios s1 y s2 definida como la suma del valor absoluto de las diferencias
         elemento a elemento de los vectores de pertenencia a macro_ids (macro_ids Belonging vectors).

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
        v1 = self.getMacroStatesBelongingVector(u1)
        v2 = self.getMacroStatesBelongingVector(u2)
        print(v1)
        print(v2)
        return float(sum([abs(x - y) for x, y in zip(v1, v2)]))

    def getMacroStatesBelongingVector(self, user_id):
        """Retorna vector de pertenencia a macro_ids (macro_ids Belonging vector) del usuario indicado.

        Parameters
        ----------
        user_id : int
            id de usuario

        Returns
        -------
        [int]
            vector de pertenencia a macro_ids (macro_ids Belonging vector) del usuario.
        """
        return getFeatureOfUser(user_id, 'UserMacroStatesBelonging')
