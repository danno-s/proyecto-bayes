from src.userempathetic.featureExtractor.features.Feature import SessionFeature
from src.userempathetic.utils.featureExtractionUtils import getAllLRSs
from src.userempathetic.utils.featureExtractionUtils import isSubContained, subsequences
from src.userempathetic.utils.sqlUtils import sqlWrapper


class SessionLRSBelongingFeature(SessionFeature):

    tablename = 'sessionlrsbelongingfeatures'
    sqlWrite = 'INSERT INTO '+tablename+ ' (session_id,vector) VALUES (%s,%s)'

    def __init__(self,session_id):
        SessionFeature.__init__(self)
        self.LRSs = getAllLRSs()
        self.vector = [0] * len(self.LRSs)
        self.session_id = int(session_id)


    def extract(self):
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from sessions where id='+str(self.session_id)
        session = sqlCD.read(sqlRead)
        assert len(session) > 0
        for row in session:
            seq = row[0].split(' ')
            subseqs = set(subsequences(seq))
            for i, lrs in enumerate(self.LRSs):
                if lrs in subseqs or isSubContained(lrs, subseqs):
                    self.vector[i] = 1

    def __str__(self):
        return "Session "+str(self.session_id)+": "+ str(self.vector) #' '.join([str("%.4f"%(x)) for x in self.histogram])

    def toSQLItem(self):
        return str(self.session_id), ' '.join([str(x) for x in self.vector])