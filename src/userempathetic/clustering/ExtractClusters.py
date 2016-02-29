#!/usr/bin/python

"""
Extrae clusters de los datos
"""

from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def createClusterExtractor():
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
    return ClusterExtractor(userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering],sessionClusteringsL=[SessionLRSBelongingClustering, SessionUserClustersBelongingClustering])

def userclustering(cE):
    cE.extractUserClusters()

def sessionclustering(cE):
    cE.extractSessionClusters()

if __name__ == '__main__':
    cE = createClusterExtractor()
    userclustering(cE)
    sessionclustering(cE)
    cE.visualizeClusters()
