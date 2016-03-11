"""
Clase ClusterExtractor

Extrae clusters de datos
"""

from src.userempathetic.view.ClusterView import ClusterView
from src.userempathetic.utils.sqlUtils import sqlWrapper


class ClusterExtractor:
    def __init__(self,sessionClusteringsConfD=None, userClusteringsConfD=None):
        """Constructor

        Parameters
        ----------
        userClusteringsConfD :{class:dict}
            Diccionario con clases UserClustering como llaves, y cuyos valores son diccionarios con valores
            de configuración del clustering.
        sessionClusteringsConfD : {class:dict}
            Diccionario con clases SessionClustering como llaves, y cuyos valores son diccionarios con valores
            de configuración del clustering.

        Returns
        -------

        """
        self.sessionClusteringsConfD = sessionClusteringsConfD or {}
        self.userClusteringsConfD = userClusteringsConfD or {}
        self.performedClusteringsL = list()
        self.userClusterD = dict()  # Diccionario con todos los clusters de usuario. La llave es la clase de UserClustering.
        self.sessionClusterD = dict()  # Diccionario con todos los clusters de sesión. La llave es la clase de SessionClustering.

    def extractUserClusters(self):
        """Recorre todos los clustering de usuarios y realiza el clustering para cada uno.

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        sqlCL.truncate('userclusters')
        for userClustering in self.userClusteringsConfD.keys():
            self.__clusterizeUsers(userClustering)
            self.printUserCluster(userClustering)

    def extractSessionClusters(self):
        """Recorre todos los clustering de sesiones y realiza el clustering para cada uno.

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        sqlCL.truncate('sessionclusters')
        for sessionClustering in self.sessionClusteringsConfD.keys():
            self.__clusterizeSessions(sessionClustering)
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
        print("\n" + str(clustering.__name__) + ":\n")
        try:
            c = clustering(confD=self.userClusteringsConfD[clustering])
            c.clusterize()
            clusters = c.getClusters()
            print('Estimated number of User clusters: %d' % c.n_clusters, '\n')
            for cluster in clusters.values():
                sqlCL.write(c.getSQLWrite(), cluster.toSQLItem())
            self.userClusterD[clustering] = c
            self.performedClusteringsL.append(clustering)
        except Exception as e:  # TODO: Crear excepcion para esto.
            print('No se obtuvieron clusters con ' + str(clustering.__name__))
            print(e)


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
        print("\n" + str(clustering.__name__) + ":\n")

        try:
            c = clustering(confD=self.sessionClusteringsConfD[clustering])
            c.clusterize()
            clusters = c.getClusters()
            print('Estimated number of Session clusters: %d' % c.n_clusters, '\n')
            for cluster in clusters.values():
                sqlCL.write(c.getSQLWrite(), cluster.toSQLItem())
            self.sessionClusterD[clustering] = c
            self.performedClusteringsL.append(clustering)
        except Exception:
            import traceback
            traceback.print_exc()
            print('No se obtuvieron clusters con ' +str(clustering.__name__))


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
                print(v.clusteringType + " Clusters")
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
                print(v.clusteringType + " Clusters")
                first = False
            print(v)

    def visualizeClusters(self):
        """Permite visualizar elementos representativos de los clusters encontrados, tanto para usuarios como de sesiones.

        Returns
        -------

        """
        cV = ClusterView()
        cV.view(self)
