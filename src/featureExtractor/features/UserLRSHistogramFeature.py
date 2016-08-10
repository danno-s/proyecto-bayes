from src.featureExtractor.features.Feature import UserFeature
from src.utils.featureExtractionUtils import getAllLRSs
from src.utils.featureExtractionUtils import isSubContained, subsequences
from src.utils.sqlUtils import sqlWrapper


class UserLRSHistogramFeature(UserFeature):
    tablename = 'userfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + \
        ' (user_id,vector,feature_name) VALUES (%s,%s,%s)'

    def __init__(self, user_id):
        UserFeature.__init__(self)
        self.LRSs = getAllLRSs()
        self.vector = [0.0] * len(self.LRSs)
        self.user_id = int(user_id)
        self.count = 0

    def extract(self):
        """Implementacion de extraccion de feature

        Returns
        -------

        """
        # Lectura de sesiones del usuario desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from sessions where user_id=' + \
            str(self.user_id)
        userSeq = sqlCD.read(sqlRead)
        assert len(userSeq) > 0
        # Calculo de histograma de uso de LRSs.
        for row in userSeq:
            seq = row[0].split(' ')
            subseqs = set(subsequences(seq))
            for i, lrs in enumerate(self.LRSs):
                if lrs in subseqs or isSubContained(lrs, subseqs):
                    self.vector[i] += 1
        # Normalizacion de frecuencias.
        self.count = sum(self.vector)
        if self.count != 0:
            self.vector = [val / self.count for val in self.vector]

    def __str__(self):
        # ' '.join([str("%.4f"%(x)) for x in self.vector])
        return str(self.user_id) + ": " + str(self.vector)

    def toSQLItem(self):
        return str(self.user_id), ' '.join([str("%.4f" % x) for x in self.vector]), self.__class__.__name__[:-7]
