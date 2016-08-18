from src.sessionComparator.SessionComparator import SessionComparator
from src.metrics.sessionMetrics.DirectMetrics import SequenceMSSDistance
from src.utils.featureExtractionUtils import getAllSessionIDs
from src.featureExtractor.features.Feature import SessionFeature


class SessionDistanceFeature(SessionFeature):
    """
    Implementacion de feature correspondiente al vector de pertenencia a LRSs (LRS Belonging vector) para una sesion.
    """
    tablename = 'sessionfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + \
        ' (session_id,vector,feature_name) VALUES (%s,%s,%s)'

    def __init__(self, session_id):
        """Constructor

        Parameters
        ----------
        session_id : int
            id de sesion.

        Returns
        -------

        """
        SessionFeature.__init__(self)
        self.s_ids = getAllSessionIDs()
        self.vector = [0] * len(self.s_ids)
        self.session_id = int(session_id)

    def extract(self):
        """Implementacion de extraccion de feature.

        Returns
        -------

        """
        for i in self.s_ids:
            sC = SessionComparator(self.session_id, i)
            self.vector[i - 1] = sC.compareSessions(SequenceMSSDistance())

    def __str__(self):
        return "Session " + str(self.session_id) + ": " + str(
            self.vector)  # ' '.join([str("%.4f"%(x)) for x in self.histogram])

    def toSQLItem(self):
        return str(self.session_id), ' '.join([str(x) for x in self.vector]), self.__class__.__name__[:-7]

if __name__ == '__main__':
    sdf = SessionDistanceFeature(3)
    sdf.extract()
    print(sdf)
