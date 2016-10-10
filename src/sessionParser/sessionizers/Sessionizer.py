from src.utils.loadConfig import Config
from src.utils.dataParsingUtils import *
from src.sessionClass.Session import Session
from src.sessionParser.sessionizers.SessionBuffer import SessionBuffer
from datetime import datetime
from abc import ABCMeta, abstractmethod


class Sessionizer:
    """
    Clase abstracta que define un objeto encargado de separar los nodos capturados en sesiones.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        self.tlimit = Config.getValue(
            attr='session_tlimit', mode='INT')  # Tiempo limite entre pasos de una sesion.

    def sessionize(self, sParser):
        """Metodo encargado de obtener sesiones a partir de los nodos cargados en el SessionParser.
        El resultado de las sesiones depende de la implementacion de bufferAccepts y toIDPair.

        Parameters
        ----------
        sParser : SessionParser
            un SessionParser con diccionario de nodos cargado.

        Returns
        -------
        [Session]
            Lista de sesiones extraidas.
        """
        # Obtener todos los usuarios.
        userL = sParser.userL
        assert len(userL) > 0
        # nodesD[user_id]= stepGen: (clickDate,macro_id, profile,microNode)
        nodesD = sParser.nodesD
        assert len(nodesD) > 0
        # Extraer sesiones para cada usuario, dado un tiempo limite entre
        # pasos.
        sessions = list()
        for user_id in userL:
            # Array of Session() objects.
            user_sessions = self.extractSessionsOf(user_id, nodesD[user_id])
            if len(user_sessions) > 0:
                for s in user_sessions:
                    sessions.append(s)
        # TODO: Agregar Excepcion NoSessionsFoundException
        assert len(sessions) > 0
        return sessions

    def extractSessionsOf(self, user_id, stepsGen):
        """Metodo encargado de obtener sesiones del usuario indicado, a partir del generador de nodos indicado.

        Parameters
        ---------
        user_id : int
            ID del usuario
        stepsGen : generator
            Generador de pasos (nodos) del usuario indicado.
        Returns
        -------

        """
        sessions = list()
        try:
            prevStep = stepsGen.__next__()
        except StopIteration:
            return sessions
        except AttributeError:
            print("AttributeError")
            return sessions
        initTime = prevStep[0]  # tiempo del primer dato.
        macro_id = prevStep[1]
        profile = prevStep[2]
        micro_id = prevStep[3]

        simulated = False
        label = None

        sb = SessionBuffer()  # Buffer de sesion.
        sb.append(self.toIDPair(macro_id, micro_id))
        for step in stepsGen:
            macro_id = step[1]
            micro_id = step[3]
            if len(step) > 4:
                simulated = step[4]
                label = step[5]
            # condicion para mantenerse en sesion actual
            if step[0] - prevStep[0] <= self.tlimit:
                if self.bufferAccepts(sb, prevStep, step):
                    # Agregar datos a sesion actual
                    sb.append(self.toIDPair(prevStep[1], prevStep[3]))
            else:
                endTime = prevStep[0]
                sb.append(self.toIDPair(prevStep[1], prevStep[3]))
                if sb.first() == sb.at(1):
                    sb.remove(0)
                sessions.append(
                    self.toSession(sb.dump(), profile, initTime, endTime, user_id, simulated=simulated, label=label))  # guardar sesion actual del usuario

                # inicializar nueva sesion
                sb.append(self.toIDPair(step[1], step[3]))
                initTime = step[0]
            prevStep = step  # actualizar step previo.
        else:
            # inicializar nueva sesion
            sb.append(self.toIDPair(macro_id, micro_id))
            endTime = prevStep[0]
            if sb.first() == sb.at(1):
                sb.remove(0)
            sessions.append(
                self.toSession(sb.dump(), profile, initTime, endTime, user_id, simulated=simulated, label=label))  # guardar ultima sesion del usuario.

        return sessions

    def toSession(self, sessionData, profile, initTime, endTime, user_id, simulated=False, label=None):
        """ Retorna un objeto Session con los datos ingresados.

        Parameters
        ----------
        sessionData : [(int,int)] | [(int,None)]
            Lista de tuplas con pares de IDs correspondiente a los datos de la sesion.
        profile : str
            Perfil del usuario de la sesion.
        initTime : int
            timestamp del tiempo de inicio de sesion.
        endTime : int
            timestamp del tiempo de termino de sesion.
        user_id : int
            ID del usuario de la sesion.

        Returns
        -------
        Session
            una Sesion con los datos cargados.
        """
        return Session(sessionData, profile=profile, initTime=datetime.fromtimestamp(initTime).isoformat(' '),
                       endTime=datetime.fromtimestamp(endTime).isoformat(' '), user_id=user_id,
                       simulated=simulated, label=label)

    @abstractmethod
    def bufferAccepts(self, sb, prevStep, step):
        """Define si el buffer acepta el paso actual como parte de la sesion o no.
        Parameters
        ----------
        sb : SessionBuffer
            Buffer de sesion
        prevStep : (int,int) | (int,None)
            paso (nodo) previo al actual.
        step : (int,int) | (int,None)
            paso (nodo) actual.
        Returns
        -------
        bool
            True si la implementacion de Sessionizer acepta el paso actual. False si no.
        """
        pass

    @abstractmethod
    def toIDPair(self, macro_id, micro_id):
        """Retorna una tupla de IDs que representa el estado de un nodo.
        Dependiendo de la implementacion del Sessionizer puede incluir o no el micro_id.

        Notes
            Una implementacion que no incluya el micro_id, debe poner None en su lugar.

        Parameters
        ----------
        macro_id : int
            ID del arbol de macro_ids del nodo.
        micro_id : int
            ID del micro estado del nodo.

        Returns
        -------

        """
        pass
