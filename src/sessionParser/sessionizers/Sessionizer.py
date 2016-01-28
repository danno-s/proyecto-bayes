from src.utils.loadConfig import Config
from src.utils.dataParsingUtils import *


class Sessionizer:
    def __init__(self):
        self.tlimit = Config().getValue(attr='session_tlimit',mode='INT')

    def extractSessionsOf(self,user_id,stepGen):
        pass

    def sessionize(self,sParser):
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL)>0
        nodesD = sParser.nodesD # nodesD[user_id]= stepGen: (clickDate,urls_id, profile,microNode)

        # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
        sessions = list()
        for user_id in userL:
            user_sessions = self.extractSessionsOf(user_id, nodesD[user_id]) # Array of Session() objects.
            if len(user_sessions)>0:
                for s in user_sessions:
                    sessions.append(s)
        assert len(sessions) > 0
        return sessions
