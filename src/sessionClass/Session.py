from src.nodeClass.Node import Node


class Session:
    def __init__(self, sequence, profile="", initTime="", endTime="", user_id=""):
        self.initTime = initTime
        self.endTime = endTime
        self.user_id = user_id

        if profile:
            self.profile = profile
        self.sequence = sequence   #string with format "1,2 2,44 3,1" (con microNodos) o "1 2 3 4" (sin microNodos)

    def __getSequenceFromNode(self,node):
        sequence = list()
        while node:
            if node.urls_id:
                if node.microNode:
                    sequence.append((node.urls_id, node.microNode))
                else:
                    sequence.append((node.urls_id,""))
            node = node.next
        return sequence

    def getFirstNode(self,s):
        """

        Parameters
        ----------
        s : a session str with format "1,2 2,44 3,1" (con microNodos) o "1 2 3 4" (sin microNodos)

        Returns
        -------
        a Node object with the nested list of the session.
        """
        steps = s.split(' ')
        firstStep = steps[0]
        tp = firstStep.split(',')
        macro_id = tp[0]
        micro_id = tp[1]
        firstNode = Node(id_user=self.user_id, profile=self.profile, id_url=macro_id,microNode=micro_id)
        currentNode = firstNode
        for step in steps[1:]:
            tp = step.split(',')
            macro_id = tp[0]
            micro_id = tp[1]
            newNode = Node(id_user=self.user_id, profile=self.profile, id_url=macro_id,microNode=micro_id)
            currentNode.addNext(newNode)
            currentNode = currentNode.next
        return firstNode



    def __str__(self):
        return str(self.profile)+":\t"+str(self.sequence) +" :\t " + str(self.initTime) +" >> "+ str(self.endTime)