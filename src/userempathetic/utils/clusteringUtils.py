from src.userempathetic.clusterClass.Cluster import Cluster
import itertools

def intersectionIDs(clusterIDs1, clusterIDs2):
    return [val for val in clusterIDs1 if val in clusterIDs2]


def combineUserClusterings(cE):
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering

    userClustersL1 = [x.ids for x in cE.userClusterD[UserLRSHistogramClustering].values()]
    userClustersL2 = [x.ids for x in cE.userClusterD[UserURLsBelongingClustering].values()]
    clusteringIntersections(userClustersL1,userClustersL2)

def clusteringIntersections(clustersL1, clustersL2):

    pairs = [x for x in itertools.product(clustersL1, clustersL2)]
    for pair in pairs:
        inter = intersectionIDs(pair[0],pair[1])
        n_intersected = len(inter)
        if n_intersected > 0:
            print(pair)
            print("Intersected Items: "+ str(n_intersected))
            print(inter)
