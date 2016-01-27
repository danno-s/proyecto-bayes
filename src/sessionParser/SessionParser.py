from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.utils.sqlUtils import sqlWrapper


class SessionParser:

    def __init__(self,s):
        assert isinstance(s,Sessionizer)
        self.nodes = list()
        self.sessionizer = s
        self.__loadNodes()
        self.sessions = list()

    def parseSessions(self):
        self.sessions = self.sessionizer.sessionize(self)

    def printSessions(self):
        for s in self.sessions:
            print(s)

    def __loadNodes(self):
        sqlCD = sqlWrapper('CD')
        rows = sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes")
        for row in rows:
            self.nodes.append((row[0],int(row[1]),row[2],row[3],row[4]))  # (clickDate, user_id, urls_id, profile, micro_id)


if __name__ == "__main__":
    from src.sessionParser.sessionizers.MacroSessionizer import MacroSessionizer
    m = SessionParser(MacroSessionizer())
    m.parseSessions()
    m.printSessions()
    print('\n')
    from src.sessionParser.sessionizers.CompleteSessionizer import CompleteSessionizer
    a = SessionParser(CompleteSessionizer())
    a.parseSessions()
    a.printSessions()
    print('\n')
    from src.sessionParser.sessionizers.FilteredSessionizer import FilteredSessionizer
    f = SessionParser(FilteredSessionizer())
    f.parseSessions()
    f.printSessions()