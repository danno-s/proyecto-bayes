from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def sessionClustering():
    cE = ClusterExtractor()
    cE.extractSessionClusters()

if __name__ == '__main__':
    sessionClustering()