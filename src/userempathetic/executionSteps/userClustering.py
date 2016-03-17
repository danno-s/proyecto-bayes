from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def userClustering():
    cE = ClusterExtractor()
    cE.extractUserClusters()

if __name__ == '__main__':
    userClustering()