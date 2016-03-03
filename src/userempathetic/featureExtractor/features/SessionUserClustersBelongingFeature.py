from src.userempathetic.featureExtractor.features.Feature import SessionFeature
from src.userempathetic.utils.clusteringUtils import getAllUserClusters
from src.userempathetic.utils.dataParsingUtils import getUserOfSession, getUserOfSimulSession


class SessionUserClustersBelongingFeature(SessionFeature):
    """
    Implementación de feature correspondiente al vector de pertenencia a User Clusters
    (UserClusters Belonging vector) para una sesión.
    """
    tablename = 'sessionuserclustersbelongingfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + ' (session_id,vector) VALUES (%s,%s)'

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
        self.userClusters = getAllUserClusters("userurlsbelongingclusters")
        self.vector = [0] * len(self.userClusters)
        self.session_id = int(session_id)
        if not self.simulation:
            self.user = getUserOfSession(self.session_id)
        else:
            self.user = getUserOfSimulSession(self.session_id)

    def extract(self):
        """Implementación de extracción de feature.

        Returns
        -------

        """
        for cluster_id, members in self.userClusters.items():
            if self.user in members:
                self.vector[cluster_id] = 1

    def extractSimulated(self):
        """Realiza exactamente lo mismo que extract.

        See Also
            extract

        Returns
        -------

        """
        self.extract()

    def __str__(self):
        return str(self.user) + ": " + str(self.vector)

    def toSQLItem(self):
        return str(self.session_id), ' '.join([str(x) for x in self.vector])