"""
Clase ClusterExtractor

Extrae clusters de datos
"""

from src.userempathetic.view.ClusterView import ClusterView
from src.userempathetic.utils.sqlUtils import sqlWrapper


class ClusterExtractor:
    def __init__(self, userClusteringsL=None, sessionClusteringsL=None):
        """Constructor

        Parameters
        ----------
        userClusteringsL : [class]
            lista de clases UserClustering
        sessionClusteringsL : [class]
            lista de clases SessionClustering

        Returns
        -------

        """
        self.userClusteringsL = userClusteringsL or []
        self.sessionClusteringsL = sessionClusteringsL or []
        self.performedClusteringsL = list()
        self.userClusterD = dict()  # Diccionario con todos los clusters de usuario. La llave es la clase de UserClustering.
        self.sessionClusterD = dict()  # Diccionario con todos los clusters de sesión. La llave es la clase de SessionClustering.

    def extractUserClusters(self):
        """Recorre todos los clustering de usuarios y realiza el clustering para cada uno.

        Returns
        -------

        """
        for userClustering in self.userClusteringsL:
            self.__clusterizeUsers(userClustering)
            self.performedClusteringsL.append(userClustering)
            self.printUserCluster(userClustering)

    def extractSessionClusters(self):
        """Recorre todos los clustering de sesiones y realiza el clustering para cada uno.

        Returns
        -------

        """
        for sessionClustering in self.sessionClusteringsL:
            self.__clusterizeSessions(sessionClustering)
            self.performedClusteringsL.append(sessionClustering)
            self.printSessionCluster(sessionClustering)

    def __clusterizeUsers(self, clustering):
        """Extrae los clusters de cada usuario y los agrega a la tabla correspondiente en la DB.

        Parameters
        ----------
        clustering : UserClustering
            clase implementación de UserClustering

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        sqlCL.truncate(clustering.tablename)
        print("\n" + str(clustering.__name__) + ":\n")
        try:
            c = clustering()
            c.clusterize()
            clusters = c.getClusters()
            print('Estimated number of User clusters: %d' % c.n_clusters, '\n')
            for cluster in clusters.values():
                sqlCL.write(c.sqlWrite, cluster.toSQLItem())
            self.userClusterD[clustering] = c
        except Exception:  # TODO: Crear excepcion para esto.
            print('No se obtuvieron clusters con ' + str(clustering.__name__))
            raise

    def __clusterizeSessions(self, clustering):
        """Extrae los clusters de cada usuario y los agrega a la tabla correspondiente en la DB.

        Parameters
        ----------
        clustering : SessionClustering
            clase implementación de SessionClustering

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        sqlCL.truncate(clustering.tablename)
        print("\n" + str(clustering.__name__) + ":\n")
        try:
            c = clustering()
            c.clusterize()
            clusters = c.getClusters()
            print('Estimated number of Session clusters: %d' % c.n_clusters, '\n')
            for cluster in clusters.values():
                sqlCL.write(c.sqlWrite, cluster.toSQLItem())
            self.sessionClusterD[clustering] = c
        except Exception:
            print('No se obtuvieron clusters con ' +str(clustering.__name__))
            raise

    def printUserCluster(self, clustering):
        """Muestra en consola los clusters encontrados para el clustering de usuarios.

        Parameters
        ----------
        clustering : UserClustering
            el tipo de clustering de usuario para imprimir.

        Returns
        -------

        """
        if clustering not in self.performedClusteringsL:
            return
        first = True
        clusterD = self.userClusterD[clustering].getClusters()
        for v in clusterD.values():
            if first:
                print(v.clusteringType.__name__ + " Clusters")
                first = False
            print(v)

    def printSessionCluster(self, clustering):
        """Muestra en consola los clusters encontrados para el clustering de sesiones.

        Parameters
        ----------
        clustering : SessionClustering
            el tipo de clustering de sesión para imprimir.

        Returns
        -------

        """
        if clustering not in self.performedClusteringsL:
            return
        first = True
        clusterD = self.sessionClusterD[clustering].getClusters()
        for v in clusterD.values():
            if first:
                print(v.clusteringType.__name__ + " Clusters")
                first = False
            print(v)

    def visualizeClusters(self):
        """Permite visualizar elementos representativos de los clusters encontrados, tanto para usuarios como de sesiones.

        Returns
        -------

        """
        cV = ClusterView()
        cV.view(self)

if __name__ == '__main__':
    from src.userempathetic.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
    from src.userempathetic.clustering.clusterings.sessionclusterings.FullSessionClustering import FullSessionClustering
    from src.userempathetic.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    from src.userempathetic.clustering.clusterings.userclusterings.FullUserClustering import FullUserClustering
    from src.userempathetic.utils.clusteringUtils import *

    cE = ClusterExtractor(sessionClusteringsL=[SessionLRSBelongingClustering, SessionUserClustersBelongingClustering,FullSessionClustering],
                          userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering, FullUserClustering])
    cE.extractUserClusters()
    cE.extractSessionClusters()
    cE.visualizeClusters()

#    print("\n\nTEST Combining clusters\n\n")
#    combineUserClusterings(cE)
