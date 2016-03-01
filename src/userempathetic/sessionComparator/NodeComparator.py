from src.userempathetic.utils.comparatorUtils import getMicroNode


class NodeComparator:
    """
    Clase que permite comparar dos nodos según distintas métricas definidas.
    """
    def __init__(self, node1, node2, metric=None):
        """Constructor

        Parameters
        ----------
        node1 : (int,int) | (int,None)
            representación de nodo según par de IDs de Macro y Micro estados.
        node2 : (int,int) | (int,None)
            representación de nodo según par de IDs de Macro y Micro estados.
        metric : NodeMetric
            (opcional) instancia de una implementación de NodeMetric.

        Returns
        -------

        """
        self.n1 = getMicroNode(node1[1])
        self.n2 = getMicroNode(node2[1])
        if metric:
            self.metric = metric

    def compareNodes(self, metric):
        """Retorna valor de comparación entre los dos nodos cargados en el NodeComparator.

        Parameters
        ----------
        metric : NodeMetric
            instancia de una implementación de NodeMetric.

        Returns
        -------
        float | int
            Valor de comparación entre los dos nodos.
        """
        return metric.compare(self)

if __name__ == '__main__':
    a= NodeComparator((1,3),(1,1))
    from src.userempathetic.metrics.microMetrics.MicroMetrics import MicroDistance
    print(a.compareNodes(MicroDistance()))