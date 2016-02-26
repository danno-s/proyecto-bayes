#!/usr/bin/python

"""
Extrae clusters de los datos
"""

from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor


def userclustering():
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    cE = ClusterExtractor(userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering])
    cE.extractUserClusters()
    cE.visualizeUserClusters()


def sessionclustering():
    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
    cE = ClusterExtractor(sessionClusteringsL=[SessionLRSBelongingClustering, SessionUserClustersBelongingClustering])
    cE.extractSessionClusters()
    cE.visualizeSessionClusters()


if __name__ == '__main__':
    userclustering()
    sessionclustering()
