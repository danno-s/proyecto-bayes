from datetime import datetime

from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.utils.dataParsingUtils import *


class MacroSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)
        pass

    def extractSessionsOf(self, user_id, stepsGen):
        sessions = list()
        try:
            prevStep = stepsGen.__next__()
        except StopIteration:
            return sessions
        initTime = prevStep[0] #tiempo del primer dato.
        macro_id = prevStep[1]
        profile = prevStep[2]

        sessionData = list()    # datos de sesión actual.
        sessionData.append((macro_id,None)) # inicializa sesión actual
        for step in stepsGen:
            macro_id = step[1]
            micro_id = step[3]
            if step[0] - prevStep[0] <= self.tlimit:   # condición para mantenerse en sesión actual
                sessionData.append((macro_id,None))                 # Agregar datos a sesión actual
            else:
                endTime = prevStep[0]
                sessions.append(self.toSession(sessionData, profile,initTime,endTime, user_id))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append((macro_id,None))     # inicializar nueva sesión
                initTime = step[0]

            prevStep = step     # actualizar timestamp previo.

        else:
            endTime = prevStep[0]
            sessions.append(self.toSession(sessionData, profile, initTime, endTime, user_id))   # guardar última sesión del usuario.

        return sessions







