from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.utils.dataParsingUtils import getAllUserIDs
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs


class ClusterExtractor:

        def __init__(self, userClusteringsL = None, sessionClusteringsL = None):
            """

            Parameters
            ----------
            userClusteringsL : lista de NOMBRES de clases UserClustering
            sessionClusteringsL: lista de NOMBRES de clases SessionClustering

            Returns
            -------

            """
            self.userClusteringsL = userClusteringsL or []
            self.sessionClusteringsL = sessionClusteringsL or []
            self.users = getAllUserIDs()
            self.sessionIDs = getAllSessionIDs()

        def extractUserClusters(self):
            for userClustering in self.userClusteringsL:
                self.__clusterizeUsers(userClustering)

        def extractSessionClusters(self):
            for sessionClustering in self.sessionClusteringsL:
                self.__clusterizeSessions(sessionClustering)

        def __clusterizeUsers(self,Clustering):
            sqlFT = sqlWrapper('FT')
            sqlFT.truncate(Clustering.tablename)
            print("\n"+str(Clustering.__name__)+":\n")
#            for user in self.users:
#                f = Clustering(user)
 #               f.extract()
  #              sqlFT.write(f.sqlWrite, f.toSQLItem())
   #             print(f)

        def __clusterizeSessions(self,clustering):
            c = clustering(self)
            c.clusterize()
            c.visualizeClusters()
