# -*- coding: utf-8 -*-

class NodeComparator:
    """
    Clase que permite comparar dos nodos segun distintas metricas definidas.
    """

    def __init__(self, node1, node2, metric=None):
        """Constructor

        Parameters
        ----------
        node1 : (int,int) | (int,None)
            representacion de nodo segun par de IDs de Macro y Micro estados.
        node2 : (int,int) | (int,None)
            representacion de nodo segun par de IDs de Macro y Micro estados.
        metric : NodeMetric
            (opcional) instancia de una implementacion de NodeMetric.

        Returns
        -------

        """
        self.n1 = node1
        self.n2 = node2
        if metric:
            self.metric = metric

    def compareNodes(self, metric):
        """Retorna valor de comparacion entre los dos nodos cargados en el NodeComparator.

        Parameters
        ----------
        metric : NodeMetric
            instancia de una implementacion de NodeMetric.

        Returns
        -------
        float | int
            Valor de comparacion entre los dos nodos.
        """
        return metric.compare(self)


if __name__ == '__main__':
    a = NodeComparator((5, 3), (3, 5))
    from src.metrics.nodeMetrics.NodeMetrics import MicroDistance
    from src.metrics.nodeMetrics.NodeMetrics import MacroDistance
    print(a.compareNodes(MacroDistance()))

 #   print(a.compareNodes(MicroDistance()))
