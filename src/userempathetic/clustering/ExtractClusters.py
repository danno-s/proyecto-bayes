from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def clustering():

    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    cE = ClusterExtractor(sessionClusteringsL = [SessionLRSBelongingClustering])
    cE.extractSessionClusters()


if __name__ == '__main__':
    clustering()