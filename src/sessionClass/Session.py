from src.nodeClass.Node import Node


class Session:
    def __init__(self,node, initTime=None, endTime=None):
        if initTime:
            self.initTime = initTime
        else:
            self.initTime = ""
        if endTime:
            self.endTime = endTime
        else:
            self.endTime = ""
        self.firstNode = node
        self.profile = self.firstNode.profile
        self.nodeSequence= self.__getNodeSequence(self.firstNode)

    def __getNodeSequence(self,node=None):
        if node is None: node = self.firstNode
        sequence = list()
        while node:
            if node.id_url:
                if node.microNode:
                    sequence.append((node.id_url, node.microNode))
                else:
                    sequence.append((node.id_url,""))
            node = node.next
        return sequence

    def __str__(self):
        return str(self.profile)+":\t "+ ' >> '.join([str(x) for x in self.nodeSequence]) +" :\t " + str(self.initTime) +" >> "+ str(self.endTime)