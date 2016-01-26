from src.sessionParser import Sessionizer
from src.nodeClass import Node
from src.nodeClass import MicroNode
from src.utils.sqlUtils import sqlWrapper

class SessionParser:

    def __init__(self,s):
        assert isinstance(s,Sessionizer)
        self.nodes = list()
        self.sessionizer = s
        self.__loadNodes()

    def parseSessions(self):
        self.sessionizer.sessionize(self)

    def __loadNodes(self):
        sqlCD = sqlWrapper('CD')
        rows = sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes")
        for row in rows:
            self.nodes.append((row[0],row[1],row[2],MicroNode(int(row[3]))))


