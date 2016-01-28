from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.nodeClass.Node import Node
from src.utils.dataParsingUtils import *

class SessionParser:

    def __init__(self,s):
        assert isinstance(s,Sessionizer)
        self.nodesD = self.__loadNodes()
        self.sessionizer = s
        self.sessions = list()
        #for k,v in self.nodesD.items():
         #   print(str(k)+": "+' '.join([str(x) for x in v]))


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
        nodesD = dict()


        for user_id in userL:
            nodesD[user_id] = self.userStepsGen(user_id)

        return nodesD

    def userStepsGen(self,user_id):
        sqlCD = sqlWrapper('CD')
        rows= sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes WHERE user_id="+str(user_id))
        for row in rows:
            yield (row[0], row[2], row[3], row[4]) # (clickDate, urls_id, profile, micro_id)


if __name__ == "__main__":
    from src.sessionParser.sessionizers.FilteredSessionizer import FilteredSessionizer
    f = SessionParser(FilteredSessionizer())
    f.parseSessions()
    f.printSessions()
    print('\n')
    from src.sessionParser.sessionizers.CompleteSessionizer import CompleteSessionizer
    a = SessionParser(CompleteSessionizer())
    a.parseSessions()
    a.printSessions()
    print('\n')
    from src.sessionParser.sessionizers.FilteredSessionizer import FilteredSessionizer
    from src.sessionParser.sessionizers.FilteredSessionizer import NullFilter
    f2 = SessionParser(FilteredSessionizer(filter=NullFilter()))
    f2.parseSessions()
    f2.printSessions()
    print('\n')
    from src.sessionParser.sessionizers.MacroSessionizer import MacroSessionizer
    m = SessionParser(MacroSessionizer())
    m.parseSessions()
    m.printSessions()
