from src.userempathetic.metrics.Metric import SessionMetric

class LRSBelongingDifference(SessionMetric):

    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self,s1,s2):
        return self.getLRSBelonging(s1) - self.getLRSBelonging(s2)

    def getLRSBelonging(self,session):
        """

        Parameters
        ----------
        session
            a Session object

        Returns
        -------
            the LRS Belonging vector of the session.
        """
        ###return session.endTime - session.initTime
        return [0,0,0,1] # SADASD
