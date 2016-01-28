from datetime import datetime

from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.nodeClass.Node import Node
from src.sessionClass.Session import Session


class FilteredSessionizer(Sessionizer):
    def __init__(self,filter=None):
        Sessionizer.__init__(self)
        if filter:
            self.filter = filter
        else:
            self.filter = MacroFilter()
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
        sessionData.append((macro_id,micro_id)) # inicializa sesión actual

        for step in stepsGen:
            macro_id = step[1]
            micro_id = step[3]
            if step[0] - prevStep[0] <= self.tlimit:   # condición para mantenerse en sesión actual
                if self.filter.filter(prevStep,step):
                    sessionData.append((prevStep[1],prevStep[3]))                 # Agregar datos a sesión actual
            else:
                endTime = prevStep[0]
                sessionData.append((prevStep[1],prevStep[3]))
                sessions.append(self.toSession(sessionData,profile,initTime,endTime,user_id))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append((step[1],step[3]))     # inicializar nueva sesión
                initTime = step[0]
            prevStep = step # actualizar step previo.
        else:
            sessionData.append((macro_id,micro_id))     # inicializar nueva sesión
            endTime = prevStep[0]
            sessions.append(self.toSession(sessionData,profile,initTime,endTime, user_id))   # guardar última sesión del usuario.

        return sessions



class Filters:
    def __init__(self):
        pass

class MacroFilter(Filters):
    def filter(self,prevStep, step):
        if prevStep[1] == step[1]:# and prevStep.profile == step.profile:
            return False
        else:
            return True

class NullFilter(Filters):
    def filter(self,prevStep,step):
        return True