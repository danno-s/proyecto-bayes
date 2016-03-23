"""
Definición de distintas Distance (implementacicones de SessionMetric) que utilizan los Features extraídos de sesiones.
"""
from src.metrics.Metric import SessionMetric
from src.utils.comparatorUtils import getFeatureOfSession


class SessionLRSBelongingDistance(SessionMetric):
    """
    Clase que implementa la métrica como una distancia entre los vectores de pertenencia a LRS (LRS Belonging vector).
    """
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        """Distancia de las sesiones s1 y s2 definida como la suma del valor absoluto de las diferencias
         elemento a elemento de los vectores de pertenencia a LRS.

        Parameters
        ----------
        s1 : Session
            una sesión.
        s2 : Session
            una sesión.
        Returns
        -------
        float
            distancia calculada.
        """
        v1 = self.getLRSBelongingVector(s1.session_id)
        v2 = self.getLRSBelongingVector(s2.session_id)
        print(v1)
        print(v2)
        return float(sum([abs(x - y) for x, y in zip(v1, v2)]))

    def getLRSBelongingVector(self, session_id):
        """Retorna el vector de pertenencia a LRS (LRS Belonging vector) de la sesion indicada.

        Parameters
        ----------
        session_id : int
            id de sesión

        Returns
        -------
        [int]
            vector de pertenencia a LRS (LRS Belonging vector) de la sesion.
        """
        return getFeatureOfSession(session_id, 'SessionLRSBelonging')


class SessionUserClustersBelongingDistance(SessionMetric):
    """
    Clase que implementa la métrica como una distancia entre los vectores de pertenencia a Clusters de Usuarios
     (UserClusters Belonging vector).
    """
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        """Distancia de las sesiones s1 y s2 definida como la suma del valor absoluto de las diferencias
         elemento a elemento de los vectores de pertenencia a clusters de usuarios.

        Parameters
        ----------
        s1 : Session
            una sesión.
        s2 : Session
            una sesión.
        Returns
        -------
        float
            distancia calculada.
        """
        v1 = self.getUserClustersBelongingVector(s1.session_id)
        v2 = self.getUserClustersBelongingVector(s2.session_id)
        if v1 or v2 is None:
            raise Exception #TODO: Crear excepción para esto.
        print(v1)
        print(v2)
        return sum([abs(x - y) for x, y in zip(v1, v2)])

    def getUserClustersBelongingVector(self, session_id):
        """Retorna el vector de pertenencia a Clusters de Usuario (UserClusters Belonging vector) de la sesion indicada.

        Parameters
        ----------
        session_id
            a Session object

        Returns
        -------
            the UserClusters Belonging vector of the session.
        """
        return getFeatureOfSession(session_id, 'SessionUserClustersBelonging')
