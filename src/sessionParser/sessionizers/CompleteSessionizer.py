from datetime import datetime

from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.sessionClass.Session import Session


class CompleteSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)
        pass

    # Obtener todos los nodos del usuario con ID user_id..
    def getNodesOf(self,user_id, nodes):
        return [(x[0],x[2],x[3],x[4]) for x in nodes if x[1] == user_id]
                                                                # (clickDate, urls_id, profile, micro_id)

    def extractSessionsOf(self, user_id, stepsGen):
        sessions = list()
        try:
            prevStep = stepsGen.__next__()
        except StopIteration:
            return sessions
        initTime = prevStep[0] #tiempo del primer dato.
        macro_id = prevStep[1]
        profile = prevStep[2]
        micro_id = prevStep[3]

        sessionData = list()    # datos de sesión actual.
        sessionData.append(str(macro_id)+","+str(micro_id)) # inicializa sesión actual
        for step in stepsGen:
            macro_id = step[1]
            micro_id = step[3]
            if step[0] - prevStep[0] <= self.tlimit:   # condición para mantenerse en sesión actual
                sessionData.append(str(macro_id)+","+str(micro_id))                 # Agregar datos a sesión actual
            else:
                endTime = prevStep[0]
                sessions.append(self.__toSession(sessionData, profile,initTime,endTime, user_id))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append(str(macro_id)+","+str(micro_id))     # inicializar nueva sesión
                initTime = step[0]

            prevStep = step     # actualizar timestamp previo.

        else:
            endTime = prevStep[0]
            sessions.append(self.__toSession(sessionData, profile, initTime, endTime, user_id))   # guardar última sesión del usuario.

        return sessions

    def __toSession(self, sessionData, profile, initTime, endTime, user_id):
        return Session(' '.join(sessionData),profile=profile,initTime=datetime.fromtimestamp(initTime).isoformat(' '), endTime=datetime.fromtimestamp(endTime).isoformat(' '),user_id=user_id)




