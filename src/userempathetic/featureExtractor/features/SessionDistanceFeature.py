from src.userempathetic.sessionComparator.SessionComparator import SessionComparator
from src.userempathetic.metrics.sessionMetrics.NodeMetrics import SequenceMSSDistance
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs
from src.userempathetic.featureExtractor.features.Feature import SessionFeature
from src.userempathetic.utils.featureExtractionUtils import isSubContained, subsequences
from src.userempathetic.utils.sqlUtils import sqlWrapper


class SessionDistanceFeature(SessionFeature):
    """
    Implementación de feature correspondiente al vector de pertenencia a LRSs (LRS Belonging vector) para una sesión.
    """
    tablename = 'sessionfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + ' (session_id,vector,feature_name) VALUES (%s,%s,%s)'

    def __init__(self, session_id, simulation=False):
        """Constructor

        Parameters
        ----------
        session_id : int
            id de sesión.

        Returns
        -------

        """
        SessionFeature.__init__(self, simulation)
        self.s_ids = getAllSessionIDs()
        self.vector = [0] * len(self.s_ids)
        self.session_id = int(session_id)

    def extract(self):
        """Implementación de extracción de feature.

        Returns
        -------

        """
        import itertools
        for i in self.s_ids:
            sC = SessionComparator(self.session_id,i)
            self.vector[i-1]= sC.compareSessions(SequenceMSSDistance())

    def extractSimulated(self):
        """Implementación de extracción de feature para sesiones simuladas.

        Returns
        -------

        """
        # Lectura de sesion simulada desde 'coreData'


        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from simulsessions where id=' + str(self.session_id)
        session = sqlCD.read(sqlRead)
        assert len(session) > 0
        for row in session:
            seq = row[0].split(' ')
            subseqs = set(subsequences(seq))
            for i, lrs in enumerate(self.LRSs):
                if lrs in subseqs or isSubContained(lrs, subseqs):
                    self.vector[i] = 1

    def __str__(self):
        return "Session " + str(self.session_id) + ": " + str(
            self.vector)  # ' '.join([str("%.4f"%(x)) for x in self.histogram])

    def toSQLItem(self):
        return str(self.session_id), ' '.join([str(x) for x in self.vector]), self.__class__.__name__[:-7]

if __name__ == '__main__':
    sdf = SessionDistanceFeature(3)
    sdf.extract()
    print(sdf)