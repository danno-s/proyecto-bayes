from src.sessionParser.sessionizers.Sessionizer import Sessionizer
from src.utils.dataParsingUtils import *


class SessionParser:

    def __init__(self,s,mode=None):
        assert isinstance(s,Sessionizer)
        self.nodesD = self.__loadNodes()
        self.sessionizer = s
        self.sessions = list()
        self.mode = mode or 'normal'

        #for k,v in self.nodesD.items():
        #    print(str(k)+": "+'\n\t'.join([str(x) for x in v]))
        #self.nodesD = self.__loadNodes()

    def parseSessions(self):
        self.sessions = self.sessionizer.sessionize(self)
        sqlCD = sqlWrapper('CD')
        sqlCD.truncate('sessions')
        sqlWrite = "INSERT INTO sessions (profile, sequence, user_id, inittime, endtime) VALUES (%s,%s,%s,%s,%s)"
        for session in self.sessions:
            sqlCD.write(sqlWrite,session.toSQLItem())

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
            if self.mode == 'simulate':
                nodesD[user_id] = self.userStepsGen(user_id,'simulatednodes')
            else:
                nodesD[user_id] = self.userStepsGen(user_id)
        return nodesD

    def userStepsGen(self,user_id,nodestable=None):
        sqlCD = sqlWrapper('CD')
        nodestable = nodestable or 'nodes'
        rows= sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from "+ nodestable+ "WHERE user_id="+str(user_id))
        for row in rows:
            yield (row[0], row[2], row[3], row[4]) # (clickDate, urls_id, profile, micro_id)
