

class UserComparator:
    """
    Clase que permite comparar dos sesiones según distintas métricas definidas.
    """

    def __init__(self, uID1, uID2):
        """Constructor

        Parameters
        ----------
        sID1 : int
            id de sesión a comparar
        sID2 : int
            id de sesión a comparar

        Returns
        -------
        """
        self.u1 = uID1
        self.u2 = uID2

    def compareUsers(self, metric):
        """Retorna valor de comparación entre los dos usuarios cargados en el UserComparator.

        Parameters
        ----------
        metric : UserMetric
            instancia de una implementación de UserMetric.

        Returns
        -------
        float | int
            Valor de comparación entre los dos usuarios.
        """
        # assert isinstance(metric,UserMetric)
        print(self.u1)
        print(self.u2)
        try:
            return metric.compare(self)
        except Exception:
            return None


if __name__ == '__main__':

    #sC = UserComparator(824, 869)
    sC = UserComparator(1, 823)
    from src.metrics.userMetrics.UserFeatureMetrics import UserLRSHistogramDistance
    from src.metrics.userMetrics.UserFeatureMetrics import UserURLsBelongingDistance

    print("UserLRSHistogramDistance = "+ str(sC.compareUsers(UserLRSHistogramDistance())))
    print("UserURLsBelongingDistance = "+ str(sC.compareUsers(UserURLsBelongingDistance())))

