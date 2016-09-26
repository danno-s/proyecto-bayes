from src.clustering.clusterings.userclusterings.\
    UserMacroStatesBelongingClustering \
    import UserMacroStatesBelongingClustering
from src.clusterClass.Cluster import Cluster
from sklearn.cluster import KMeans
import numpy as np

class UMSBCKMeans(UserMacroStatesBelongingClustering):
    """
    UserMacroStatesBelongingClustering que usa el algoritmo de k-means
    en vez de DBSCAN para calcular los clusters.
    """

    def __init__(self, confD=None):
        UserMacroStatesBelongingClustering.__init__(self, confD=confD)

    def initClusteringAlgorithm(self):
        return KMeans(
            n_clusters=self.confD['kmeans']['n_clusters']
        )

    def clusterize(self):
        """
        Utiliza el algotimo de clustering KMeans sobre los datos para
        encontrar clusters. Los resultados quedan almacenados en la instancia
        del clustering que ejecuta esta funcion.
        :return:
        """

        if self.X is None:
            raise Exception
        self.clusteringAlgorithm.fit(self.X)

        centers = self.clusteringAlgorithm.cluster_centers_
        unique_labels = set(self.clusteringAlgorithm.labels_)
        self.n_clusters = len(unique_labels)

        for k in unique_labels:
            class_member_mask = (self.clusteringAlgorithm.labels_ == k)

            xy = [(x, cl_id) for x, cl_id, i, in zip(
                self.X, self.ids, class_member_mask) if i]
            if k != -1:
                self.clustersD[k] = Cluster(
                    vectors=[j[0] for j in xy],
                    ids=[j[1] for j in xy],
                    label=k,
                    clusteringType=self.__class__.__name__,
                    center=centers[k]
                )
        self.outliers = []

if __name__ == '__main__':
    from src.utils.loadConfig import Config
    conf = Config.getUserClusteringsConfigD()
    cl = UMSBCKMeans(
        confD=Config.getUserClusteringsConfigD()[UserMacroStatesBelongingClustering]
    )
    cl.clusterize()
    print(cl)
