from src.nodeClass.Node import Node

class Session:
    def __init__(self,node):
        self.firstNode = Node()
        self.nodeSequence= self.__getNodeSequence(self.firstNode)

    def __getNodeSequence(self):

        nextNode = self.firstNode.next
        sequence = list()
        while nextNode != []:
            sequence.append((nextNode.urls_id,nextNode.profile))


a = [Node(url=1,profile='23123')]
b = []

print(a != [])