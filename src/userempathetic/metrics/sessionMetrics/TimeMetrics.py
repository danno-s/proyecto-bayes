from datetime import timedelta

from src.userempathetic.metrics.Metric import SessionMetric


class DurationDistance(SessionMetric):
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        return abs(self.getDuration(s1) - self.getDuration(s2))

    def getDuration(self, session):
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
        return td / timedelta(seconds=1)


# return td

class HourOfDayDistance(SessionMetric):
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        return abs(self.getHourOfDay(s1) - self.getHourOfDay(s2))

    def getHourOfDay(self, session):
        """

        Parameters
        ----------
        session
            a Session object

        Returns
        -------
            the total duration of the session in seconds.
        """
        hour = session.initTime.hour + session.initTime.minute / 60.
        print(hour)
        return hour / 24.0

# return td
