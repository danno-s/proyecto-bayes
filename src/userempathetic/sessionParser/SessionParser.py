"""
Elemento encargado de separar los nodos capturados en sesiones. La forma en que se definen las sesiones queda determinada
por el Sessionizer utilizado.
"""

from src.userempathetic.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.userempathetic.utils.dataParsingUtils import *


class SessionParser:
    """
    Clase encargada de cargar nodos y utilizar un Sessionizer para obtener sesiones.
    También guarda las sesiones en la tabla correspondiente.
    """
    def __init__(self, sessionizer):
        """Constructor del SessionParser. Requiere indicarle el Sessionizer a utilizar.

        Parameters
        ----------
        sessionizer : Sessionizer
            una instancia de alguna clase que extienda Sessionizer.

        Returns
        -------

        """
        assert isinstance(sessionizer, Sessionizer)
        self.__loadNodes() # carga self.nodesD con los generadores de nodos capturados asociados a cada usuario.
        self.sessionizer = sessionizer
        self.sessions = list()

    def parseSessions(self):
        """Método que obtiene sesiones desde el Sessionizer y las guarda en la tabla de la DB.

        Returns
        -------

        """
        self.sessions = self.sessionizer.sessionize(self)
        sqlCD = sqlWrapper('CD')
        sqlCD.truncate('sessions')
        sqlWrite = "INSERT INTO sessions (profile, sequence, user_id, inittime, endtime) VALUES (%s,%s,%s,%s,%s)"
        for session in self.sessions:
            sqlCD.write(sqlWrite, session.toSQLItem())

    def printSessions(self):
        """Imprime en consola las sesiones contenidas en el SessionParser.

        Returns
        -------

        """
        for s in self.sessions:
            print(s)

    def __loadNodes(self):
        """Carga variable de instancia self.nodesD con diccionario [user_id] = generador de nodos (steps).

        Returns
        -------

        """
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL) > 0
        # Extraer datos de nodos para cada usuario
        self.nodesD = dict()
        for user_id in userL:
            self.nodesD[user_id] = self.userStepsGen(user_id)


    def userStepsGen(self, user_id):
        """ Generador que permite obtener todos los nodos capturados del usuario indicado.

        Parameters
        ----------
        user_id : int
            id del usuario

        Yields
        ----------
        tuple
            (clickDate, urls_id, profile, micro_id)
        Returns
        -------

        """
        sqlCD = sqlWrapper('CD')
        rows = sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes WHERE user_id=" + str(user_id))
        for row in rows:
            yield (row[0], row[2], row[3], row[4])  # (clickDate, urls_id, profile, micro_id)
