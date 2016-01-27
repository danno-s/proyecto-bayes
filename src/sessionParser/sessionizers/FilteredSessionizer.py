from datetime import datetime

from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.utils.dataParsingUtils import *


class FilteredSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)
        self.filter = LastMacroIDStepFilter()
        pass

    # Obtener todos los nodos del usuario con ID user_id..
    def getNodesOf(self,user_id, nodes):
        return [(x[0],x[2],x[3],x[4]) for x in nodes if x[1] == user_id]
                                                                # (clickDate, urls_id, profile, micro_id)

    def extractFilteredSessionsOf(self,user_id,nodes):
        sessions = list()
        userSessions= self.getNodesOf(user_id,nodes)
        if len(userSessions) == 0: return sessions
        profile = userSessions[0][2]
        prevStep = userSessions[0]
        initTime = prevStep[0] #tiempo del primer dato.
        macro_id = prevStep[1]
        micro_id = prevStep[3]

        sessionData = list()    # datos de sesión actual.

        for i, step in enumerate(userSessions[1:]):
            macro_id = step[1]
            micro_id = step[3]
            if step[0] - prevStep[0] <= self.tlimit:   # condición para mantenerse en sesión actual
                if self.filter.accepts(prevStep,step):
                    sessionData.append([prevStep[1],prevStep[3]])                 # Agregar datos a sesión actual
            else:
                endTime = prevStep[0]

                sessions.append(self.__toSession(profile,sessionData,initTime,endTime))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append([prevStep[1],prevStep[3]])     # inicializar nueva sesión
                initTime = step[0]

            prevStep = step # actualizar step previo.
        else:
            sessionData.append([macro_id,micro_id])     # inicializar nueva sesión
            endTime = step[0]
            sessions.append(self.__toSession(profile,sessionData,initTime,endTime))   # guardar última sesión del usuario.

        return sessions

    def sessionize(self,sParser):
        nodes = sParser.nodes # (clickDate, user_id, urls_id, profile,micro_id)
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL)>0

        # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
        sessions = dict()
        for user_id in userL:
            user_sessions = self.extractFilteredSessionsOf(user_id,nodes)
            if len(user_sessions)>0:
                sessions[user_id] =user_sessions
        assert len(sessions) > 0

        ss = ((k, x[0], x[1], x[2].isoformat(' '), x[3].isoformat(' ')) for k in sessions.keys() for x in sessions[k])

        return ss

    def __toSession(self, profile, sessionData, initTime, endTime):
        return profile,' '.join([','.join([str(i) for i in x]) for x in sessionData]), datetime.fromtimestamp(initTime), datetime.fromtimestamp(endTime)


class StepFilter:

    def __init__(self): pass

class LastMacroIDStepFilter(StepFilter):

    def accepts(self,prevStep, step):
        if prevStep[1] == step[1]:
            return False
        else:
            return True



