from src.featureExtractor.features.Feature import SessionFeature
from src.utils.featureExtractionUtils import getAllLRSs
from src.utils.featureExtractionUtils import isSubContained, subsequences
from src.utils.sqlUtils import sqlWrapper


class SessionLRSBelongingFeature(SessionFeature):
    """
    Implementación de feature correspondiente al vector de pertenencia a LRSs (LRS Belonging vector) para una sesión.
    """
    tablename = 'sessionfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + \
        ' (session_id,vector,feature_name) VALUES (%s,%s,%s)'

    def __init__(self, session_id):
        """Constructor

        Parameters
        ----------
        session_id : int
            id de sesión.

        Returns
        -------

        """
        SessionFeature.__init__(self)
        self.LRSs = getAllLRSs()
        self.vector = [0] * len(self.LRSs)
        self.session_id = int(session_id)

    def extract(self):
        """Implementación de extracción de feature.

        Returns
        -------

        """
        # Lectura de sesion desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select sequence from sessions where id=' + \
            str(self.session_id)
        session = sqlCD.read(sqlRead)
        assert len(session) > 0
        # Cálculo de subsecuencias y correspondencia con uso de LRSs.
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