from src.utils.clusteringUtils import getUserClusters, \
    getPerformedUserClusterings
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

        X = []
        Y = []
        for label, cluster in self.user_clusters.items():
            for vector in cluster.vectors:
                X.append(vector)
                Y.append(label)
                print(vector)
        self.algorithm.fit(X, Y)

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
        cluster = self.algorithm.predict(features)
        return cluster


