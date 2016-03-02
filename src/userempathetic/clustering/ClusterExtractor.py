"""
Clase ClusterExtractor

Extrae clusters de datos
"""

from matplotlib import pyplot as plt
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
        self.userClusterD = dict()  # Diccionario con todos los clusters de usuario. La llave es la clase de UserClustering.
        self.sessionClusterD = dict() # Diccionario con todos los clusters de sesión. La llave es la clase de SessionClustering.

    def extractUserClusters(self):
        """Recorre todos los clustering de usuarios y realiza el clustering para cada uno.

        Returns
        -------

        """
        for userClustering in self.userClusteringsL:
            self.__clusterizeUsers(userClustering)
        self.printUserClusters()

    def extractSessionClusters(self):
        """Recorre todos los clustering de sesiones y realiza el clustering para cada uno.

        Returns
        -------

        """
        for sessionClustering in self.sessionClusteringsL:
            self.__clusterizeSessions(sessionClustering)
        self.printSessionClusters()

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
        c.clusterize()
        clusters = c.getClusters()
        self.userClusterD[clustering] = clusters
        print('Estimated number of User clusters: %d' % c.n_clusters, '\n')
        for cluster in clusters.values():
            sqlCL.write(c.sqlWrite, cluster.toSQLItem())

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

    def printSessionClusters(self):

        for clustering in self.sessionClusteringsL:
            first = True
            for v in self.sessionClusterD[clustering].values():
                if first:
                    print(v.clusteringType.__name__ + " Clusters")
                    first = False
                print(v)

    def printUserClusters(self):
        for clustering in self.userClusteringsL:
            first = True
            for v in self.userClusterD[clustering].values():
                if first:
                    print(v.clusteringType.__name__ + " Clusters")
                    first = False
                print(v)

    def visualizeClusters(self):
        i = 0
        for clustering in self.userClusteringsL:
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
                                   yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]], capsize=3,
                                   markersize=8)

                    ax[k].text(1.01, 0.5, '#' + str(k),
                               verticalalignment='center', horizontalalignment='left',
                               transform=ax[k].transAxes,
                               color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                    ax[k].text(1.05, 0.5, "  ("+ str(v.size) + ")",
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
                                   yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]], capsize=3,
                                   markersize=8)
                    ax[k].text(1.01, 0.5, '#' + str(k),
                               verticalalignment='center', horizontalalignment='left',
                               transform=ax[k].transAxes,
                               color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                    ax[k].text(1.05, 0.5, "  ("+ str(v.size) + ")",
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
        i = 0
        for clustering in self.userClusteringsL:
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
                                   yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]], capsize=3,
                                   markersize=8)

                    ax[k].text(1.01, 0.5, '#' + str(k),
                               verticalalignment='center', horizontalalignment='left',
                               transform=ax[k].transAxes,
                               color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                    ax[k].text(1.05, 0.5, "  ("+ str(v.size) + ")",
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
        i = 0
        for clustering in self.sessionClusteringsL:
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
                                   yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]], capsize=3,
                                   markersize=8)
                    ax[k].text(1.01, 0.5, '#' + str(k),
                               verticalalignment='center', horizontalalignment='left',
                               transform=ax[k].transAxes,
                               color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                    ax[k].text(1.05, 0.5, "  ("+ str(v.size) + ")",
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
    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    from src.userempathetic.utils.clusteringUtils import *

    cE = ClusterExtractor(sessionClusteringsL=[SessionLRSBelongingClustering, SessionUserClustersBelongingClustering],
                          userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering])
    cE.extractUserClusters()
    cE.extractSessionClusters()
    cE.visualizeClusters()

    print("\n\nTEST Combining clusters\n\n")
    combineUserClusterings(cE)
