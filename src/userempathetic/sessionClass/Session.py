"""
Clase Session, representa una sesión en el sistema
"""

from src.userempathetic.nodeClass.Node import Node


class Session:

    def __init__(self, sequence, profile="", initTime="", endTime="", user_id=""):
        self.initTime = initTime
        self.endTime = endTime
        self.user_id = user_id
        self.profile = profile
        self.sequence = sequence   # lista de tuplas (urls_id, micro_id), o (urls_id, None)

    def __getSequenceFromNode(self,node):
        sequence = list()
        while node:
            if node.urls_id:
                if node.microNode:
                    sequence.append((node.urls_id, node.microNode))
                else:
                    sequence.append((node.urls_id,None))
            node = node.next
        return sequence

    def getFirstNode(self,steps = None):
        """

        Parameters
        ----------
        steps : lista de tuplas (urls_id, micro_id), o (urls_id, None)

        Returns
        -------
        a Node object with the nested list of the session.
        """
        if not steps:
            steps = self.sequence

        firstStep = steps[0]
        macro_id = firstStep[0]
        micro_id = firstStep[1]
        firstNode = Node(id_user=self.user_id, profile=self.profile, id_url=macro_id,microNode=micro_id)
        currentNode = firstNode
        for step in steps[1:]:
            macro_id = step[0]
            micro_id = step[1]
            newNode = Node(id_user=self.user_id, profile=self.profile, id_url=macro_id,microNode=micro_id)
            currentNode.addNext(newNode)
            currentNode = currentNode.next
        return firstNode

    def accept(self, visitor):
        visitor.metSession(self)


    def __str__(self):
        return str(self.profile)+":\t"+self.__sequenceToStr(self.sequence) +" ;\t " + str(self.initTime) +" >> "+ str(self.endTime)

    def __sequenceToStr(self,sequence):
        tps = list()
        for x in sequence:
            if x[1]:
                tps.append("("+ str(x[0])+","+str(x[1])+")")
            else:
                tps.append("("+ str(x[0])+")")
        s = ' >> '.join(tps)
        return s

    def toSQLItem(self):
        #(profile, sequence, user_id, inittime, endtime)
        steps = list()
        for x in self.sequence:
            if x[1]:
                step=str(x[0])+","+str(x[1])
            else:
                step=str(x[0])
            steps.append(step)
        return (self.profile,' '.join(steps),self.user_id,self.initTime,self.endTime)
