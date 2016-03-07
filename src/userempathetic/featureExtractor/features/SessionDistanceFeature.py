from src.userempathetic.sessionComparator.SessionComparator import SessionComparator
from src.userempathetic.metrics.sessionMetrics.NodeMetrics import SequenceMSSDistance
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs
from src.userempathetic.featureExtractor.features.Feature import SessionFeature
from src.userempathetic.utils.featureExtractionUtils import isSubContained, subsequences
from src.userempathetic.utils.sqlUtils import sqlWrapper

#TODO: COMPLETAR IMPLEMENTACIÓN DE ESTA CLASE
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
        for i in self.s_ids:
            sC = SessionComparator(self.session_id,i)
            self.vector[i-1]= sC.compareSessions(SequenceMSSDistance())

    def extractSimulated(self):
        """Implementación de extracción de feature para sesiones simuladas.

        Returns
        -------

        """
        for i in self.s_ids:
            sC = SessionComparator(self.session_id,i,simulation=True)
            self.vector[i-1]= sC.compareSessions(SequenceMSSDistance())

    def __str__(self):
        return "Session " + str(self.session_id) + ": " + str(
            self.vector)  # ' '.join([str("%.4f"%(x)) for x in self.histogram])

    def toSQLItem(self):
        return str(self.session_id), ' '.join([str(x) for x in self.vector]), self.__class__.__name__[:-7]

if __name__ == '__main__':
    sdf = SessionDistanceFeature(3)
    sdf.extract()
    print(sdf)