#!/usr/bin/python

"""
Extrae clusters de los datos
"""

from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def clustering():

    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.SessionUserClustersBelongingClustering import SessionUserClustersBelongingClustering

    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering

    cE = ClusterExtractor(sessionClusteringsL = [SessionLRSBelongingClustering,SessionUserClustersBelongingClustering],userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering])
    cE.extractSessionClusters()
    cE.extractUserClusters()
    cE.visualizeClusters()




if __name__ == '__main__':
    clustering()