from datetime import datetime

from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.utils.dataParsingUtils import *
from src.nodeClass.Node import Node
from src.sessionClass.Session import Session


class FilteredSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)
        self.filter = LastMacroIDStepFilter()
        pass

    # Obtener todos los nodos del usuario con ID user_id..
    def getNodesOf(self,user_id, nodes):
        return [(x[0],x[2],x[3],x[4]) for x in nodes if x[1] == user_id]
                                                                # (clickDate, urls_id, profile, micro_id)

    def extractFilteredSessionsOf(self,nodesL):
        sessions = list()
        if len(nodesL) == 0: return sessions
        profile = nodesL[0].profile
        firstNode = nodesL[0]

        prevStep = firstNode    # datos de sesión actual.
        initTime = prevStep.clickdate #tiempo del primer dato.
        macro_id = prevStep.urls_id
        micro_id = prevStep.microNode

        for i, step in enumerate(nodesL[1:]):
            macro_id = step.urls_id
            micro_id = step.microNode
            if step.clickdate - prevStep.clickdate <= self.tlimit:   # condición para mantenerse en sesión actual
                if self.filter.accepts(prevStep,step):
                    prevStep.addNext(step)                 # Agregar datos a sesión actual
            else:
                endTime = prevStep.clickdate
                prevStep.addNext(step)
                sessions.append(self.__toSession(profile,firstNode,initTime,endTime))  # guardar sesión actual del usuario
                firstNode = step     # inicializar nueva sesión
                initTime = step.clickdate

            prevStep = step # actualizar step previo.
        else:
            sessionData.append([macro_id,micro_id])     # inicializar nueva sesión
            endTime = prevStep.clickdate
            sessions.append(self.__toSession(profile, sessionData, initTime, endTime))   # guardar última sesión del usuario.

        return sessions

    def sessionize(self,sParser):
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL)>0
        nodesD = sParser.nodesD # Node(clickDate, user_id, urls_id, profile,microNode)

        # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
        sessions = list()
        for user_id in userL:
            user_sessions = self.extractFilteredSessionsOf(nodesD[user_id]) # Array of Session() objects.
            if len(user_sessions)>0:
                for s in user_sessions:
                    sessions.append(s)
        assert len(sessions) > 0
        return sessions

    def getFirstNode(self,s):
        """

        Parameters
        ----------
        s : a session tuple with format (profile, sessionData, initTime, endTime)

        Returns
        -------
        a Node object with the nested list of the session.
        """
        steps = s[2].split(' ')
        firstStep = steps[0]
        tp = firstStep.split(',')
        macro_id = tp[0]
        micro_id = tp[1]
        firstNode = Node(id_user=s[0], profile=s[1], id_url=macro_id, microNode=micro_id)
        currentNode = firstNode
        for step in steps[1:]:
            tp = step.split(',')
            macro_id = tp[0]
            micro_id = tp[1]
            newNode = Node(id_user=s[0], profile=s[1], id_url=macro_id, microNode=micro_id)
            currentNode.addNext(newNode)
            currentNode = currentNode.next
        return firstNode

    def __toSession(self, profile, sessionData, initTime, endTime):
        #return profile,' '.join([','.join([str(i) for i in x]) for x in sessionData]), datetime.fromtimestamp(initTime).isoformat(' '), datetime.fromtimestamp(endTime).isoformat(' ')
        return Session(sessionData,initTime=datetime.fromtimestamp(initTime).isoformat(' '), endTime=datetime.fromtimestamp(endTime).isoformat(' '))

class StepFilter:

    def __init__(self): pass

class LastMacroIDStepFilter(StepFilter):

    def accepts(self,prevStep, step):
        if prevStep.urls_id == step.urls_id:# and prevStep.profile == step.profile:
            return False
        else:
            return True


