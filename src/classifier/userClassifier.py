from src.utils.clusteringUtils import getUserClusters, \
    getPerformedUserClusterings
from src.featureExtraction.ExtractFeatures import extractPostClusteringFeatures
from sklearn.linear_model import LogisticRegression


class UserClassifier(object):
    """
    Clase encargada de clasificar usuarios con un cluster especifico.
    El algoritmo usado para clasificar es Logistic Regression.
    """

    def __init__(self, clustering):
        """

        :param clustering:
            El clustering con el cual se desea clasificar.
        """
        self.algorithm = LogisticRegression()

        self.user_clusters = getUserClusters(clustering)
        self.user_features = extractPostClusteringFeatures()

        print(type(self.user_clusters))
        print(type(self.user_features))


    def predict(self, features):
        """

        :param features:
            Features del usuario al cual se quiere clasificar.
            Estas deben ser o bien Macrostate belonging vector, o
            LRS Histogram.
        :return: Int
            Se retorna el cluster al cual el usuario pertenece según el
            clasificador.

        """
        return 0

if __name__ == "__main__":
    # Macrostate belonging cluster
    cl = getPerformedUserClusterings()[0]
    uc = UserClassifier(cl)


