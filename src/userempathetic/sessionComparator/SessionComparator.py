from src.userempathetic.sessionClass.Session import Session
from src.userempathetic.nodeClass.Node import Node
from src.userempathetic.nodeClass.MicroNode import MicroNode
from src.userempathetic.utils.sqlUtils import sqlWrapper
# from src.userempathetic.metrics.Metric import SessionMetric


def initSession(session_id):
    raw_session = getRawSessionData(session_id)
    sequence = raw_session[0].split(' ')
    if ',' not in raw_session[0]:
        session_type = 'macro'
        for i, macroid in enumerate(sequence):
            sequence[i] = (macroid, None)
    else:
        session_type = 'full'
        for i, pair in enumerate(sequence):
            pair = pair.split(',')
            sequence[i] = (pair[0], pair[1])
    profile = int(raw_session[1])
    user_id = int(raw_session[4])
    inittime = raw_session[2]
    endtime = raw_session[3]

    return Session(sequence, profile=profile, initTime=inittime, endTime=endtime, user_id=user_id,
                   session_id=session_id)


def getRawSessionData(session_id, sessionTable='sessions'):
    sqlCD = sqlWrapper('CD')
    row = sqlCD.read(
        "SELECT sequence,profile,inittime,endtime,user_id FROM " + sessionTable + " WHERE id = " + str(session_id))
    return row[0]


class SessionComparator:
    def __init__(self, sID1, sID2):
        self.s1 = initSession(sID1)
        self.s2 = initSession(sID2)
        print(self.s1)
        print(self.s2)

    def compareSessions(self, metric):  # que metrica usar...
        # assert isinstance(metric,SessionMetric)
        return metric.compare(self)


if __name__ == '__main__':
    sC = SessionComparator(1, 25)
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
