from src.userempathetic.metrics.Metric import SessionMetric
from src.userempathetic.utils.comparatorUtils import getMSS
from src.userempathetic.sessionComparator.NodeComparator import NodeComparator
from src.userempathetic.metrics.MicroMetrics.MicroMetrics import MicroDistance
#MSS = Maximum Shared Sequence

class MacroSequenceMSSDistance(SessionMetric):
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        v1,v2, c  = getMSS(s1,s2)
        print(v1)
        print(v2)
        print(c)
        #return abs(len(s1.sequence) -len(s2.sequence)) + sum(c) - len(c)
        return sum(c) + len(s2.sequence)+len(s1.sequence)-2*len(c)

class SequenceMSSDistance(SessionMetric):
    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        v1,v2, c  = getMSS(s1,s2)
        print(v1)
        print(v2)
        print(c)
        nodeDist = 0
        for n1,n2 in zip(v1,v2):
            nC = NodeComparator(n1,n2)
            microDistance= nC.compareNodes(MicroDistance())
            nodeDist += microDistance
        return sum(c)+ len(s2.sequence)+len(s1.sequence)-2*len(c) + nodeDist
