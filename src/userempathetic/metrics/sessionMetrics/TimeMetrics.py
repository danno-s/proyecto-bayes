from src.userempathetic.metrics.Metric import SessionMetric
from datetime import timedelta
from datetime import datetime


class DurationDifference(SessionMetric):

    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self,s1,s2):
        return self.getDuration(s1) - self.getDuration(s2)

    def getDuration(self,session):
        """

        Parameters
        ----------
        session
            a Session object

        Returns
        -------
            the total duration of the session in seconds.
        """
        td = session.endTime - session.initTime
        return td/timedelta(seconds=1)
#        return td
