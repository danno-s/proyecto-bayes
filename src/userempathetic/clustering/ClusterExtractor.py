"""
Clase ClusterExtractor

Extrae clusters de datos
"""

from matplotlib import pyplot as plt


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
        c = clustering()
        try:
            c.clusterize()
            clusters = c.getClusters()
            self.userClusterD[clustering] = clusters
            print('Estimated number of User clusters: %d' % c.n_clusters, '\n')
            for cluster in clusters.values():
                sqlCL.write(c.sqlWrite, cluster.toSQLItem())
        except Exception:  # TODO: Crear excepcion para esto.
            print('No se obtuvieron clusters con ' + str(clustering.__name__))

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
        c = clustering()
        c.clusterize()
        clusters = c.getClusters()
        self.sessionClusterD[clustering] = c.getClusters()
        print('Estimated number of Session clusters: %d' % c.n_clusters, '\n')
        for cluster in clusters.values():
            sqlCL.write(c.sqlWrite, cluster.toSQLItem())

    def printUserCluster(self, clustering):
        """Muestra en consola los clusters encontrados para el clustering de usuarios.

        Parameters
        ----------
        clustering : UserClustering
            el tipo de clustering de usuario para imprimir.

        Returns
        -------

        """
        first = True
        for v in self.userClusterD[clustering].values():
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
        first = True
        for v in self.sessionClusterD[clustering].values():
            if first:
                print(v.clusteringType.__name__ + " Clusters")
                first = False
            print(v)

    def visualizeClusters(self):
        """Permite visualizar elementos representativos de los clusters encontrados, tanto para usuarios como de sesiones.

        Returns
        -------

        """
        i = 0
        for clustering in self.userClusteringsL:
            if clustering in self.performedClusteringsL:
                n = len(self.userClusterD[clustering])
                if n > 1:
                    f1, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f1.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f1.axes[:-1]], visible=False)
                    features_dim = self.userClusterD[clustering][0].features_dim
                    for k, v in self.userClusterD[clustering].items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                       yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
                                       capsize=3,
                                       markersize=8)

                        ax[k].text(1.01, 0.5, '#' + str(k),
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                        ax[k].text(1.05, 0.5, "  (" + str(v.size) + ")",
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='green', fontsize=10, rotation='horizontal')
                    plt.xlim([-0.2, features_dim - 1 + 0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n / 2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f1.suptitle(clustering.__name__)

        for clustering in self.sessionClusteringsL:
            if clustering in self.performedClusteringsL:
                n = len(self.sessionClusterD[clustering])
                if n > 1:
                    f2, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f2.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f2.axes[:-1]], visible=False)
                    features_dim = self.sessionClusterD[clustering][0].features_dim
                    for k, v in self.sessionClusterD[clustering].items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                       yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
                                       capsize=3,
                                       markersize=8)
                        ax[k].text(1.01, 0.5, '#' + str(k),
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                        ax[k].text(1.05, 0.5, "  (" + str(v.size) + ")",
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='green', fontsize=10, rotation='horizontal')

                    plt.xlim([-0.2, features_dim - 1 + 0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n / 2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f2.suptitle(clustering.__name__)
        plt.show()

    def visualizeUserClusters(self):
        """Permite visualizar elementos representativos de los clusters encontrados sólo para usuarios.
        Returns
        -------

        """
        i = 0
        for clustering in self.userClusteringsL:
            if clustering in self.performedClusteringsL:
                n = len(self.userClusterD[clustering])
                if n > 1:
                    f1, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f1.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f1.axes[:-1]], visible=False)
                    features_dim = self.userClusterD[clustering][0].features_dim
                    for k, v in self.userClusterD[clustering].items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                       yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
                                       capsize=3,
                                       markersize=8)

                        ax[k].text(1.01, 0.5, '#' + str(k),
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                        ax[k].text(1.05, 0.5, "  (" + str(v.size) + ")",
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='green', fontsize=10, rotation='horizontal')
                    plt.xlim([-0.2, features_dim - 1 + 0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n / 2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f1.suptitle(clustering.__name__)
        plt.show()

    def visualizeSessionClusters(self):
        """Permite visualizar elementos representativos de los clusters encontrados sólo para sesiones.

        Returns
        -------

        """
        i = 0
        for clustering in self.sessionClusteringsL:
            if clustering in self.performedClusteringsL:
                n = len(self.sessionClusterD[clustering])
                if n > 1:
                    f2, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f2.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f2.axes[:-1]], visible=False)
                    features_dim = self.sessionClusterD[clustering][0].features_dim
                    for k, v in self.sessionClusterD[clustering].items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                       yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
                                       capsize=3,
                                       markersize=8)
                        ax[k].text(1.01, 0.5, '#' + str(k),
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                        ax[k].text(1.05, 0.5, "  (" + str(v.size) + ")",
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='green', fontsize=10, rotation='horizontal')
                    plt.xlim([-0.2, features_dim - 1 + 0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n / 2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f2.suptitle(clustering.__name__)
        plt.show()


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
