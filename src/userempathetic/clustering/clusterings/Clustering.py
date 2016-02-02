class Clustering:
    def __init__(self):
        pass

    def getCentroid(self,cluster):
        N = len(cluster[0])
        return [sum([value[x]/len(cluster) for value in cluster]) for x in range(N)]

    def getMax(self,cluster):
        N = len(cluster[0])
        return [max([value[x] for value in cluster]) for x in range(N)]

    def getMin(self,cluster):
        N = len(cluster[0])
        return [min([value[x] for value in cluster]) for x in range(N)]


class SessionClustering(Clustering):
    pass


class UserClustering(Clustering):
    pass