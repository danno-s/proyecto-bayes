from src.userempathetic.utils.comparatorUtils import getSession


class SessionComparator:
    """
    Clase que permite comparar dos sesiones según distintas métricas definidas.
    """

    def __init__(self, sID1, sID2):
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
        self.s1 = getSession(sID1)
        self.s2 = getSession(sID2)

    def compareSessions(self, metric):
        """Retorna valor de comparación entre los dos sesiones cargadas en el SessionComparator.

        Parameters
        ----------
        metric : SessionMetric
            instancia de una implementación de SessionMetric.

        Returns
        -------
        float | int
            Valor de comparación entre las dos sesiones.
        """
        # assert isinstance(metric,SessionMetric)
        print(self.s1)
        print(self.s2)
        return metric.compare(self)


if __name__ == '__main__':
    # sC = SessionComparator(1, 3)
    # sC = SessionComparator(1,41)
    # sC = SessionComparator(1,44)
    # sC = SessionComparator(35,45)

    sC = SessionComparator(1, 3)
    '''
    from src.userempathetic.metrics.sessionMetrics.TimeMetrics import DurationDistance
    from src.userempathetic.metrics.sessionMetrics.TimeMetrics import HourOfDayDistance

    from src.userempathetic.metrics.sessionMetrics.FeatureMetrics import SessionLRSBelongingDistance
    from src.userempathetic.metrics.sessionMetrics.FeatureMetrics import SessionUserClustersBelongingDistance

    durationDistance = sC.compareSessions(DurationDistance())
    print("DurationDistance = " + str(durationDistance) + " seconds.")
    hourOfDayDistance = sC.compareSessions(HourOfDayDistance())
    print("HourOfDaysDistance = " + str(hourOfDayDistance) + " [hours of the day]")
    lrsbelongingDistance = sC.compareSessions(SessionLRSBelongingDistance())
    print("LRSBelongingDistance = " + str(lrsbelongingDistance))
    userclustersbelongingDistance = sC.compareSessions(SessionUserClustersBelongingDistance())
    print("UserClustersBelongingDistance = " + str(userclustersbelongingDistance))
    '''

    from src.userempathetic.metrics.sessionMetrics.NodeMetrics import MacroSequenceMSSDistance

    macroseqMSSDistance = sC.compareSessions(MacroSequenceMSSDistance())
    print("MacroSequenceMSSDistance = " + str(macroseqMSSDistance) + ".")

    from src.userempathetic.metrics.sessionMetrics.NodeMetrics import SequenceMSSDistance

    seqMSSDistance = sC.compareSessions(SequenceMSSDistance())
    print("SequenceMSSDistance = " + str(seqMSSDistance) + ".")
