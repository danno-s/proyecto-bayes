from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.nodeClass.Node import Node
from src.utils.dataParsingUtils import *

class SessionParser:

    def __init__(self,s):
        assert isinstance(s,Sessionizer)
        self.nodesD = dict()
        self.__loadNodes()
        self.sessionizer = s

        self.sessions = list()

    def parseSessions(self):
        self.sessions = self.sessionizer.sessionize(self)

    def printSessions(self):
        for s in self.sessions:
            print(s)
    def __loadNodes(self):
        # Obtener todos los usuarios.
        userL = getAllUserIDs()
        assert len(userL)>0

        # Extraer datos de nodos para cada usuario
        userSessionsD = dict()
        sqlCD = sqlWrapper('CD')

        for user_id in userL:
            #rows= sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes WHERE user_id="+str(user_id))
            rows= sqlCD.read("SELECT * from nodes WHERE user_id="+str(user_id))
            user_steps = [Node(str=row) for row in rows]                            #(row[0],int(row[1]),row[2],row[3],row[4]) for row in rows] # (clickDate, user_id, urls_id, profile, micro_id)
            if len(user_steps)>0:
                self.nodesD[user_id] = user_steps

        #for k,v in self.nodesD.items():
        #    print(str(k)+": "+' '.join([str(x) for x in v]))


if __name__ == "__main__":
    from src.sessionParser.sessionizers.FilteredSessionizer import FilteredSessionizer
    f = SessionParser(FilteredSessionizer())
    f.parseSessions()
    f.printSessions()
 #   print('\n')
#    from src.sessionParser.sessionizers.CompleteSessionizer import CompleteSessionizer
#    a = SessionParser(CompleteSessionizer())
#    a.parseSessions()
#    a.printSessions()
#    print('\n')
#    from src.sessionParser.sessionizers.MacroSessionizer import MacroSessionizer
#    m = SessionParser(MacroSessionizer())
#    m.parseSessions()
#    m.printSessions()
