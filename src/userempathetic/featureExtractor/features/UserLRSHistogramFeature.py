from src.userempathetic.featureExtractor.features.Feature import UserFeature
from src.userempathetic.utils.featureExtractionUtils import getAllLRSs
from src.userempathetic.utils.featureExtractionUtils import isSubContained, subsequences
from src.userempathetic.utils.sqlUtils import sqlWrapper


class UserLRSHistogramFeature(UserFeature):
    tablename = 'userlrshistogramfeatures'
    sqlWrite = 'INSERT INTO '+tablename+ ' (user_id,histogram,count) VALUES (%s,%s,%s)'

    def __init__(self,user):
        UserFeature.__init__(self)
        self.LRSs = getAllLRSs()
        self.histogram = [0.0] * len(self.LRSs)
        self.user = int(user)
        self.count = 0
        pass

    def extract(self):
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from sessions where user_id='+str(self.user)
        userSeq = sqlCD.read(sqlRead)
        assert len(userSeq) > 0
        for row in userSeq:
            seq = row[0].split(' ')
            subseqs = set(subsequences(seq))
            for i, lrs in enumerate(self.LRSs):
                if lrs in subseqs or isSubContained(lrs, subseqs):
                    self.histogram[i] += 1

        self.count = sum(self.histogram)
        if self.count != 0:
            self.histogram = [val/self.count for val in self.histogram]


    def __str__(self):
        return str(self.user)+": "+ str(self.histogram) #' '.join([str("%.4f"%(x)) for x in self.histogram])

    def toSQLItem(self):
        return str(self.user), ' '.join([str("%.4f"%(x)) for x in self.histogram]), str(self.count)
