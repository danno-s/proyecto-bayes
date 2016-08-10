

class UserComparator:
    """
    Clase que permite comparar dos usuarios segun distintas metricas definidas.
    """

    def __init__(self, uID1, uID2):
        """Constructor

        Parameters
        ----------
        uID1 : int
            id de usuario a comparar
        uID2 : int
            id de usuario a comparar

        Returns
        -------
        """
        self.u1 = uID1
        self.u2 = uID2

    def compareUsers(self, metric):
        """Retorna valor de comparacion entre los dos usuarios cargados en el UserComparator.

        Parameters
        ----------
        metric : UserMetric
            instancia de una implementacion de UserMetric.

        Returns
        -------
        float | int
            Valor de comparacion entre los dos usuarios.
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
    uC = UserComparator(1, 824)
    from src.metrics.userMetrics.UserFeatureMetrics import UserLRSHistogramDistance
    from src.metrics.userMetrics.UserFeatureMetrics import UserURLsBelongingDistance

    print("UserLRSHistogramDistance = " +
          str(uC.compareUsers(UserLRSHistogramDistance())))
    print("UserURLsBelongingDistance = " +
          str(uC.compareUsers(UserURLsBelongingDistance())))
