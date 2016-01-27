from src.sessionParser.Sessionizer import Sessionizer
from src.nodeClass.Node import Node
from src.utils.loadConfig import Config
from datetime import datetime
from src.utils.dataParsingUtils import *

class MacroSessionizer(Sessionizer):
    def __init__(self):
        self.tlimit = Config().getValue(attr='session_tlimit',mode='INT')

    # Obtener todos los nodos del usuario con ID user_id..
    def getNodesOf(self,user_id, nodes):
        return [(x[2],x[0]) for x in nodes if x[1] == user_id]  #(urls_id, clickDate)

    def extractMacroSessionsOf(self,user_id,nodes):
        profile = getProfileOf(user_id)
        sessions = list()
        userSessions= self.getNodesOf(user_id,nodes)
        if len(userSessions)==0:    return sessions
        tprev = userSessions[0][1]   #tiempo del primer dato.
        initTime = datetime.fromtimestamp(tprev)
        macro_id = userSessions[0][0]

        sessionData = list()    # datos de sesión actual.
        sessionData.append(macro_id) # inicializa sesión actual
        for i, step in enumerate(userSessions[1:]):
            macro_id = step[0]
            if step[1] - tprev <= self.tlimit:   # condición para mantenerse en sesión actual
                sessionData.append(macro_id)                 # Agregar datos a sesión actual
            else:
                endTime = datetime.fromtimestamp(tprev)

                sessions.append((profile,' '.join([str(x) for x in sessionData]),initTime,endTime))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append(macro_id)     # inicializar nueva sesión
                initTime = datetime.fromtimestamp(step[1])

            tprev = step[1]     # actualizar timestamp previo.

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
            user_sessions = self.extractMacroSessionsOf(user_id,nodes)
            if len(user_sessions)>0:
                sessions[user_id] =user_sessions
        assert len(sessions) > 0

        ss = ((k, x[0], x[1], x[2].isoformat(' '), x[3].isoformat(' ')) for k in sessions.keys() for x in sessions[k])

        return ss




