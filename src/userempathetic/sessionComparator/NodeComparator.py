from src.userempathetic.nodeClass.MicroNode import MicroNode
from src.userempathetic.utils.comparatorUtils import getMicroNode


class NodeComparator:
    def __init__(self, node1, node2, metric=None):
        self.n1 = getMicroNode(node1[1])
        self.n2 = getMicroNode(node2[1])
        if metric:
            self.metric = metric

    def compareNodes(self, metric):
        return metric.compare(self)

if __name__ == '__main__':
    a= NodeComparator((1,3),(1,1))
    from src.userempathetic.metrics.MicroMetrics.MicroMetrics import MicroDistance
    print(a.compareNodes(MicroDistance()))