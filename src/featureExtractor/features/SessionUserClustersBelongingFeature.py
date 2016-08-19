from src.featureExtractor.features.Feature import SessionFeature
from src.utils.clusteringUtils import getAllUserClusters
from src.utils.dataParsingUtils import getUserOfSession


class SessionUserClustersBelongingFeature(SessionFeature):
    """
    Implementacion de feature correspondiente al vector de pertenencia a User Clusters
    (UserClusters Belonging vector) para una sesion.
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
        self.userClusters = getAllUserClusters("UserMacroStatesBelonging")
        self.vector = [0] * len(self.userClusters)
        self.session_id = int(session_id)
        self.user = getUserOfSession(self.session_id)

    def extract(self):
        """Implementacion de extraccion de feature.

        Returns
        -------

        """
        for cluster_id, members in self.userClusters.items():
            if self.user in members:
                self.vector[cluster_id] = 1
                break

    def __str__(self):
        return str(self.session_id) + ": [" + str(self.user) + "]" + str(self.vector)

    def toSQLItem(self):
        if len(self.vector) == 0:
            v = None
        else:
            v = ' '.join([str(x) for x in self.vector])
        return str(self.session_id), v, self.__class__.__name__[:-7]
