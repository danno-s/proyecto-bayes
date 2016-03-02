from src.simulated.sessionParser.sessionizers.Sessionizer import Sessionizer
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
        sqlCD.truncate('simulsessions')
        sqlWrite = "INSERT INTO simulsessions (profile, sequence, user_id, inittime, endtime) VALUES (%s,%s,%s,%s,%s)"
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
            self.nodesD[user_id] = simulUserStepsGen(user_id)

