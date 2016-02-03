from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def clustering():

    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering

    cE = ClusterExtractor(sessionClusteringsL = [SessionLRSBelongingClustering],userClusteringsL=[UserURLsBelongingClustering])
    cE.extractSessionClusters()
    cE.extractUserClusters()
    cE.visualizeClusters()




if __name__ == '__main__':
    clustering()