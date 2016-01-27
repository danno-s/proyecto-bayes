from datetime import datetime

from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.utils.dataParsingUtils import *


class CompleteSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)
        pass

    # Obtener todos los nodos del usuario con ID user_id..
    def getNodesOf(self,user_id, nodes):
        return [(x[0],x[2],x[3],x[4]) for x in nodes if x[1] == user_id]
                                                                # (clickDate, urls_id, profile, micro_id)

    def extractCompleteSessionsOf(self,user_id,nodes):
        profile = nodes[0][2]
        sessions = list()
        userSessions= self.getNodesOf(user_id,nodes)
        if len(userSessions)==0:    return sessions
        firstStep = userSessions[0]
        tprev = firstStep[0]   #tiempo del primer dato.
        initTime = datetime.fromtimestamp(tprev)
        macro_id = firstStep[1]
        micro_id = firstStep[3]

        sessionData = list()    # datos de sesión actual.
        sessionData.append((macro_id,micro_id)) # inicializa sesión actual
        for i, step in enumerate(userSessions[1:]):
            macro_id = step[1]
            micro_id = step[3]
            if step[0] - tprev <= self.tlimit:   # condición para mantenerse en sesión actual
                sessionData.append((macro_id,micro_id))                 # Agregar datos a sesión actual
            else:
                endTime = datetime.fromtimestamp(tprev)

                sessions.append((profile,' '.join([str(x) for x in sessionData]),initTime,endTime))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append((macro_id,micro_id))     # inicializar nueva sesión
                initTime = datetime.fromtimestamp(step[0])

            tprev = step[0]     # actualizar timestamp previo.

        else:
            endTime = datetime.fromtimestamp(tprev)
            sessions.append((profile,' '.join([str(x) for x in sessionData]), initTime, endTime))   # guardar última sesión del usuario.

        return sessions

    def sessionize(self,sParser):
        nodes = sParser.nodes # (clickDate, user_id, urls_id, profile,micro_id)
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL)>0

        # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
        sessions = dict()
        for user_id in userL:
            user_sessions = self.extractCompleteSessionsOf(user_id,nodes)
            if len(user_sessions)>0:
                sessions[user_id] =user_sessions
        assert len(sessions) > 0

        ss = ((k, x[0], x[1], x[2].isoformat(' '), x[3].isoformat(' ')) for k in sessions.keys() for x in sessions[k])

        return ss




