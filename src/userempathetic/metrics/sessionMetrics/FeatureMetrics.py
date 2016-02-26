from src.userempathetic.metrics.Metric import SessionMetric
from src.userempathetic.utils.comparatorUtils import getFeatureOfSession


class SessionLRSBelongingDistance(SessionMetric):
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        v1 = self.getLRSBelongingVector(s1.session_id)
        v2 = self.getLRSBelongingVector(s2.session_id)
        print(v1)
        print(v2)
        return sum([abs(x - y) for x, y in zip(v1, v2)])

    def getLRSBelongingVector(self, session_id):
        """

        Parameters
        ----------
        session_id
            a Session object

        Returns
        -------
            the LRS Belonging vector of the session.
        """
        return getFeatureOfSession(session_id, 'SessionLRSBelonging')


class SessionUserClustersBelongingDistance(SessionMetric):
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        v1 = self.getUserClustersBelongingVector(s1.session_id)
        v2 = self.getUserClustersBelongingVector(s2.session_id)
        print(v1)
        print(v2)
        return sum([abs(x - y) for x, y in zip(v1, v2)])

    def getUserClustersBelongingVector(self, session_id):
        """

        Parameters
        ----------
        session_id
            a Session object

        Returns
        -------
            the UserClusters Belonging vector of the session.
        """
        return getFeatureOfSession(session_id, 'SessionUserClustersBelonging')
