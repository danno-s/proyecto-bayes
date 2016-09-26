"""
Clase ClusterExtractor

Extrae clusters de datos
"""

from src.view.ClusterView import ClusterView
from src.utils.sqlUtils import sqlWrapper
from src.utils.loadConfig import Config


class ClusterExtractor:

    def __init__(self):
        """Constructor

        Parameters
        ----------
        userClusteringsConfD :{class:dict}
            Diccionario con clases UserClustering como llaves, y cuyos valores
            son diccionarios con valores de configuracion del clustering.
        sessionClusteringsConfD : {class:dict}
            Diccionario con clases SessionClustering como llaves, y cuyos
            valores son diccionarios con valores de configuracion del
            clustering.

        Returns
        -------

        """

        self.sessionClusteringsConfD = Config.getSessionClusteringsConfigD()
        self.userClusteringsConfD = Config.getUserClusteringsConfigD()
        self.performedClusteringsL = list()
        # Diccionario con todos los clusters de usuario. La llave es la clase
        # de UserClustering.
        self.userClusterD = dict()
        # Diccionario con todos los clusters de sesion. La llave es la clase de
        # SessionClustering.
        self.sessionClusterD = dict()

    def extractUserClusters(self):
        """
        Recorre todos los clustering de usuarios y realiza el clustering para
        cada uno.

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        sqlCL.truncate('userclusters')
        for userClustering in self.userClusteringsConfD.keys():
            self.__clusterizeUsers(userClustering)
            self.printUserCluster(userClustering)

    def extractSessionClusters(self):
        """
        Recorre todos los clustering de sesiones y realiza el clustering para
        cada uno.

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        sqlCL.truncate('sessionclusters')
        for sessionClustering in self.sessionClusteringsConfD.keys():
            self.__clusterizeSessions(sessionClustering)
            self.printSessionCluster(sessionClustering)

    def __clusterizeUsers(self, clustering):
        """
        Extrae los clusters de cada usuario y los agrega a la tabla
        correspondiente en la DB.

        Parameters
        ----------
        clustering : UserClustering
            clase implementacion de UserClustering

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
            outliers = c.getOutliers()
            sqlCL.write(c.getSQLWrite(), outliers.toSQLItem())
            self.userClusterD[clustering] = c
            self.performedClusteringsL.append(clustering)
        except Exception as e:  # TODO: Crear excepcion para esto.
            import traceback
            traceback.print_exc()
            print('No se obtuvieron clusters con ' + str(clustering.__name__))
            print(e)

    def __clusterizeSessions(self, clustering):
        """
        Extrae los clusters de cada usuario y los agrega a la tabla
        correspondiente en la DB.

        Parameters
        ----------
        clustering : SessionClustering
            clase implementacion de SessionClustering

        Returns
        -------

        """
        sqlCL = sqlWrapper('CL')
        print("\n" + str(clustering.__name__) + ":\n")

        try:
            c = clustering(confD=self.sessionClusteringsConfD[clustering])
            c.clusterize()
            clusters = c.getClusters()
            print('Estimated number of Session clusters: %d' %
                  c.n_clusters, '\n')
            for cluster in clusters.values():
                sqlCL.write(c.getSQLWrite(), cluster.toSQLItem())
            outliers = c.getOutliers()
            sqlCL.write(c.getSQLWrite(), outliers.toSQLItem())
            self.sessionClusterD[clustering] = c
            self.performedClusteringsL.append(clustering)
        except AssertionError:
            print('No se obtuvieron clusters con ' + str(clustering.__name__))
        except:
            import traceback
            traceback.print_exc()


    def printUserCluster(self, clustering):
        """
        Muestra en consola los clusters encontrados para el clustering de
        usuarios.

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

    def printAllUserClusters(self):
        for clustering in self.performedClusteringsL:
            self.printUserCluster(clustering)

    def printSessionCluster(self, clustering):
        """
        Muestra en consola los clusters encontrados para el clustering de
        sesiones.

        Parameters
        ----------
        clustering : SessionClustering
            el tipo de clustering de sesion para imprimir.

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

if __name__ == "__main__":
    ce = ClusterExtractor()
    ce.extractUserClusters()
    ce.printAllUserClusters()
