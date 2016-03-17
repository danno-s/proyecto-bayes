"""
Elemento encargado de separar los nodos capturados en sesiones. La forma en que se definen las sesiones queda
determinada por el Sessionizer utilizado.
"""

from src.userempathetic.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.userempathetic.utils.dataParsingUtils import *


class SessionParser:
    """
    Clase encargada de cargar nodos y utilizar un Sessionizer para obtener sesiones.
    También guarda las sesiones en la tabla correspondiente.
    """

    def __init__(self, sessionizer, simulation=False):
        """Constructor del SessionParser. Requiere indicarle el Sessionizer a utilizar.

        Parameters
        ----------
        sessionizer : Sessionizer
            una instancia de alguna clase que extienda Sessionizer.

        Returns
        -------

        """
        assert isinstance(sessionizer, Sessionizer)
        if simulation:
            self.simulation = simulation
        if not simulation:
            self.simulation = False
            self.__loadNodes()  # carga self.nodesD con los generadores de nodos capturados asociados a cada usuario.
        else:
            self.__loadSimulNodes()
        self.sessionizer = sessionizer
        self.sessions = list()

    def parseSessions(self):
        """Método que obtiene sesiones desde el Sessionizer y las guarda en la tabla correspondiente de la DB,
        dependiendo del parámetro 'simulation' del SessionParser.

        Returns
        -------

        """
        self.sessions = self.sessionizer.sessionize(self)
        sqlCD = sqlWrapper('CD')
        if self.simulation: # Borrar sólo los datos simulados anteriores.
            readParams = "profile, sequence, user_id, inittime, endtime"
            sqlWrite = "INSERT INTO sessions (profile, sequence, user_id, inittime, endtime) VALUES " \
                                                     "(%s,%s,%s,%s,%s)"
            sqlCD.truncateSimulated('sessions',readParams, sqlWrite)

            sqlWrite = "INSERT INTO sessions (profile, sequence, user_id, inittime, endtime, simulated, label) VALUES " \
            "(%s,%s,%s,%s,%s,%s,%s)"
            for session in self.sessions:
                sqlCD.write(sqlWrite, session.toSQLItem() + (True,None))#TODO: Agregar label de clustering.                                                     "(%s,%s,%s,%s,%s,%s,%s)"
        else:               # Borrar toda la tabla.
            sqlCD.truncate('sessions')
            sqlWrite = "INSERT INTO sessions (profile, sequence, user_id, inittime, endtime) VALUES " \
                                                     "(%s,%s,%s,%s,%s)"
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
        self.userL = getAllUserIDs()
        assert len(self.userL) > 0
        # Extraer datos de nodos para cada usuario
        self.nodesD = dict()
        for user_id in self.userL:
            self.nodesD[user_id] = userStepsGen(user_id)

    def __loadSimulNodes(self):
        """Carga variable de instancia self.nodesD con diccionario [user_id] = generador de nodos simulados (steps).

        Returns
        -------

        """
        # Obtener todos los usuarios.
        self.userL = getAllSimulUserIDs()
        assert len(self.userL) > 0
        # Extraer datos de nodos para cada usuario
        self.nodesD = dict()
        for user_id in self.userL:
            self.nodesD[user_id] = simulUserStepsGen(user_id)

