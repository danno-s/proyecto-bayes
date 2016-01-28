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
                sessionData.append([prevStep[1],prevStep[3]])
                sessions.append(self.__toSession(profile,sessionData,initTime,endTime))  # guardar sesión actual del usuario

                sessionData.clear()
                sessionData.append([step[1],step[3]])     # inicializar nueva sesión
                initTime = step[0]

            prevStep = step # actualizar step previo.
        else:
            sessionData.append([macro_id,micro_id])     # inicializar nueva sesión
            endTime = prevStep[0]
            sessions.append(self.__toSession(profile,sessionData,initTime,endTime))   # guardar última sesión del usuario.

        return sessions

    def sessionize(self,sParser):
        nodes = sParser.nodes # (clickDate, user_id, urls_id, profile,micro_id)
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL)>0

        # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
        userSessionsD = dict()
        for user_id in userL:
            user_steps = self.extractFilteredSessionsOf(user_id,nodes)
            if len(user_steps)>0:
                userSessionsD[user_id] = user_steps
        assert len(userSessionsD) > 0
        #(k, x[0], x[1], x[2], x[3])
        sessions = list()
        for k in userSessionsD.keys():
            for x in userSessionsD[k]:
                s = (k,x[0],x[1],x[2],x[3])
                node = self.getFirstNode(s)
                sessions.append(Session(node,initTime=s[3],endTime=s[4]))
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
        firstNode = Node(id_user=s[0], profile=s[1], id_url=macro_id,microNode=micro_id)
        currentNode = firstNode
        for step in steps[1:]:
            tp = step.split(',')
            macro_id = tp[0]
            micro_id = tp[1]
            newNode = Node(id_user=s[0], profile=s[1], id_url=macro_id,microNode=micro_id)
            currentNode.addNext(newNode)
            currentNode = currentNode.next
        return firstNode

    def __toSession(self, profile, sessionData, initTime, endTime):
        return profile,' '.join([','.join([str(i) for i in x]) for x in sessionData]), datetime.fromtimestamp(initTime).isoformat(' '), datetime.fromtimestamp(endTime).isoformat(' ')


class StepFilter:

    def __init__(self): pass

class LastMacroIDStepFilter(StepFilter):

    def accepts(self,prevStep, step):
        if prevStep[1] == step[1]:
            return False
        else:
            return True


