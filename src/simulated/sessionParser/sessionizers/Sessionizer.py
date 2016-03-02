from src.userempathetic.utils.loadConfig import Config
from src.userempathetic.utils.dataParsingUtils import *
from src.userempathetic.sessionClass.Session import Session
from src.simulated.sessionParser.sessionizers.SessionBuffer import SessionBuffer
from datetime import datetime
from abc import ABCMeta, abstractmethod


class Sessionizer:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.tlimit = Config().getValue(attr='session_tlimit', mode='INT')

    def sessionize(self, sParser):
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL) > 0
        nodesD = sParser.nodesD  # nodesD[user_id]= stepGen: (clickDate,urls_id, profile,microNode)

        # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
        sessions = list()
        for user_id in userL:
            user_sessions = self.extractSessionsOf(user_id, nodesD[user_id])  # Array of Session() objects.
            if len(user_sessions) > 0:
                for s in user_sessions:
                    sessions.append(s)
        assert len(sessions) > 0
        return sessions

    def extractSessionsOf(self, user_id, stepsGen):
        sessions = list()
        try:
            prevStep = stepsGen.__next__()
        except StopIteration:
            return sessions
        initTime = prevStep[0]  # tiempo del primer dato.
        macro_id = prevStep[1]
        profile = prevStep[2]
        micro_id = prevStep[3]

        sb = SessionBuffer()
        sb.append(self.toIDPair(macro_id, micro_id))
        for step in stepsGen:
            macro_id = step[1]
            micro_id = step[3]
            if step[0] - prevStep[0] <= self.tlimit:  # condición para mantenerse en sesión actual
                if self.bufferAccepts(sb, prevStep, step):
                    sb.append(self.toIDPair(prevStep[1], prevStep[3]))  # Agregar datos a sesión actual
            else:
                endTime = prevStep[0]
                sb.append(self.toIDPair(prevStep[1], prevStep[3]))
                if sb.first() == sb.at(1):
                    sb.remove(0)
                sessions.append(
                    self.toSession(sb.dump(), profile, initTime, endTime, user_id))  # guardar sesión actual del usuario

                sb.append(self.toIDPair(step[1], step[3]))  # inicializar nueva sesión
                initTime = step[0]
            prevStep = step  # actualizar step previo.
        else:
            sb.append(self.toIDPair(macro_id, micro_id))  # inicializar nueva sesión
            endTime = prevStep[0]
            if sb.first() == sb.at(1):
                sb.remove(0)
            sessions.append(
                self.toSession(sb.dump(), profile, initTime, endTime, user_id))  # guardar última sesión del usuario.

        return sessions

    def toSession(self, sessionData, profile, initTime, endTime, user_id):
        return Session(sessionData, profile=profile, initTime=datetime.fromtimestamp(initTime).isoformat(' '),
                       endTime=datetime.fromtimestamp(endTime).isoformat(' '), user_id=user_id)

    @abstractmethod
    def bufferAccepts(self, sb, prevStep, step):
        pass

    @abstractmethod
    def toIDPair(self, macro_id, micro_id):
        pass
