from src.userempathetic.featureExtractor.features.Feature import UserFeature
from src.userempathetic.utils.featureExtractionUtils import getAllLRSs
from src.userempathetic.utils.featureExtractionUtils import isSubContained, subsequences
from src.userempathetic.utils.sqlUtils import sqlWrapper


class UserLRSHistogramFeature(UserFeature):
    tablename = 'userlrshistogramfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + ' (user_id,histogram,count) VALUES (%s,%s,%s)'

    def __init__(self, user_id, simulation=False):
        UserFeature.__init__(self, simulation)
        self.LRSs = getAllLRSs()
        self.histogram = [0.0] * len(self.LRSs)
        self.user_id = int(user_id)
        self.count = 0

    def extract(self):
        """Implementación de extracción de feature

        Returns
        -------

        """
        # Lectura de sesiones del usuario desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from sessions where user_id=' + str(self.user_id)
        userSeq = sqlCD.read(sqlRead)
        assert len(userSeq) > 0
        # Cálculo de histograma de uso de LRSs.
        for row in userSeq:
            seq = row[0].split(' ')
            subseqs = set(subsequences(seq))
            for i, lrs in enumerate(self.LRSs):
                if lrs in subseqs or isSubContained(lrs, subseqs):
                    self.histogram[i] += 1
        # Normalización de frecuencias.
        self.count = sum(self.histogram)
        if self.count != 0:
            self.histogram = [val / self.count for val in self.histogram]

    def extractSimulated(self):
        """Implementación de extracción de feature para usuarios simulados

        Returns
        -------

        """
        # Lectura de sesiones simuladas del usuario desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from simulsessions where user_id=' + str(self.user_id)
        userSeq = sqlCD.read(sqlRead)
        assert len(userSeq) > 0
        # Cálculo de histograma de uso de LRSs.
        for row in userSeq:
            seq = row[0].split(' ')
            subseqs = set(subsequences(seq))
            for i, lrs in enumerate(self.LRSs):
                if lrs in subseqs or isSubContained(lrs, subseqs):
                    self.histogram[i] += 1
        # Normalización de frecuencias.
        self.count = sum(self.histogram)
        if self.count != 0:
            self.histogram = [val / self.count for val in self.histogram]

    def __str__(self):
        return str(self.user_id) + ": " + str(self.histogram)  # ' '.join([str("%.4f"%(x)) for x in self.histogram])

    def toSQLItem(self):
        return str(self.user_id), ' '.join([str("%.4f" % x) for x in self.histogram]), str(self.count)
