"""
Clase ClusterExtractor

Extrae clusters de datos
"""

from src.userempathetic.utils.sqlUtils import sqlWrapper
from matplotlib import pyplot as plt


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
            self.userClusterD = dict()
            self.sessionClusterD = dict()

        def extractUserClusters(self):
            for userClustering in self.userClusteringsL:
                self.__clusterizeUsers(userClustering)
            self.printUserClusters()

        def extractSessionClusters(self):
            for sessionClustering in self.sessionClusteringsL:
                self.__clusterizeSessions(sessionClustering)
            self.printSessionClusters()

        def __clusterizeUsers(self,clustering):
            c = clustering()
            c.clusterize()
            self.userClusterD[clustering]=c.getClusters()
            print('Estimated number of User clusters: %d' % c.n_clusters)

        # """
        # def __clusterizeUsers(self,clustering):
        #     sqlFT = sqlWrapper('FT')
        #     sqlFT.truncate(clustering.tablename)
        #     print("\n"+str(clustering.__name__)+":\n")
        #     for user in self.users:
        #         f = clustering(user)
        #         f.extract()
        #         sqlFT.write(f.sqlWrite, f.toSQLItem())
        #         print(f)
        # """

        def __clusterizeSessions(self,clustering):
            c = clustering()
            c.clusterize()
            self.sessionClusterD[clustering]=c.getClusters()
            print('Estimated number of Session clusters: %d' % c.n_clusters)

        def printSessionClusters(self):

            for clustering in self.sessionClusteringsL:
                first = True
                for v in self.sessionClusterD[clustering].values():
                    if first:
                        print(v.clusteringType.__name__ +" Clusters")
                        first = False
                    print(v)

        def printUserClusters(self):
            for clustering in self.userClusteringsL:
                first = True
                for v in self.userClusterD[clustering].values():
                    if first:
                        print(v.clusteringType.__name__ +" Clusters")
                        first = False
                    print(v)

        def visualizeClusters(self):
            i = 0
            for clustering in self.userClusteringsL:
                n = len(self.userClusterD[clustering])
                if n > 1:
                    f1, ax = plt.subplots(n, sharex=True, sharey=True,num=i)
                    i+=1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f1.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f1.axes[:-1]], visible=False)
                    features_dim= self.userClusterD[clustering][0].features_dim
                    for k,v in self.userClusterD[clustering].items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c,fmt='b.',ecolor='r', yerr=[low,up],capsize=3,markersize=8)

                        ax[k].text(1.01, 0.5, '#' +str(k),
                                verticalalignment='center', horizontalalignment='left',
                                transform=ax[k].transAxes,
                                color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                    plt.xlim([-0.2,features_dim-1+0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n/2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f1.suptitle(clustering.__name__)

            for clustering in self.sessionClusteringsL:
                n = len(self.sessionClusterD[clustering])
                if n > 1:
                    f2, ax = plt.subplots(n, sharex=True, sharey=True,num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f2.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f2.axes[:-1]], visible=False)
                    features_dim= self.sessionClusterD[clustering][0].features_dim
                    for k,v in self.sessionClusterD[clustering].items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c,fmt='b.',ecolor='r', yerr=[low,up],capsize=3,markersize=8)
                        ax[k].text(1.01, 0.5, '#' +str(k),
                                verticalalignment='center', horizontalalignment='left',
                                transform=ax[k].transAxes,
                                color='red', fontsize=10, fontweight='bold', rotation='horizontal')

                    plt.xlim([-0.2,features_dim-1+0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n/2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f2.suptitle(clustering.__name__)
            plt.show()

if __name__ == '__main__':
    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    from src.userempathetic.utils.clusteringUtils import *


    cE = ClusterExtractor(sessionClusteringsL = [SessionLRSBelongingClustering],userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering])
    cE.extractSessionClusters()
    cE.extractUserClusters()
   # cE.visualizeClusters()

    print("\n\nTEST QL\n\n")
    combineUserClusterings(cE)

