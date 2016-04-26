# -*- coding: utf-8 -*-

"""
Definición de distintas Distance (implementacicones de SessionMetric) que utilizan comparación directa de los nodos
de las sesiones.
"""
from src.metrics.Metric import SessionMetric
from src.utils.comparatorUtils import getMSS
from src.sessionComparator.NodeComparator import NodeComparator
from src.metrics.nodeMetrics.NodeMetrics import MicroDistance


# MSS = Maximum Shared Sequence

class MacroSequenceMSSDistance(SessionMetric):
    """
    Clase que implementa la métrica como una heurística calculada en base a los MSS y considera únicamente los
    macro estados de los nodos.
    """

    def __init__(self):
        SessionMetric.__init__(self)

    def distance(self, s1, s2):
        """Distancia de las sesiones s1 y s2 definida como la cantidad de nodos que no tienen en común, MÁS la cantidad
         de nodos saltados para poder obtener los MSS (ver documentación de getMSS)

        See Also
            getMSS

        Parameters
        ----------
        s1 : Session
            una sesión.
        s2 : Session
            una sesión.
        Returns
        -------
        float
            distancia calculada.
        """
        v1, v2, c = getMSS(s1, s2)
        print(v1)
        print(v2)
        print(c)
        return sum(c) + len(s2.sequence) + len(s1.sequence) - 2 * len(c)


class SequenceMSSDistance(SessionMetric):
    """
    Clase que implementa la métrica como una heurística calculada en base a los MSS y considera los
    macro estados y micro estados de los nodos.
    """

    def __init__(self):
        SessionMetric.__init__(self)
        self.alpha = 1.0
        self.beta = 1.0

    def distance(self, s1, s2):
        """Distancia de las sesiones s1 y s2 definida como la cantidad de nodos que no tienen en común, MÁS la cantidad
         de nodos saltados para poder obtener los MSS (ver documentación de getMSS), MÁS la distancia entre los
         micro estados de los nodos de MSS.

        See Also
            getMSS

        Parameters
        ----------
        s1 : Session
            una sesión.
        s2 : Session
            una sesión.
        Returns
        -------
        float
            distancia calculada.
        """
        v1, v2, c = getMSS(s1, s2)
        # print(v1)
        # print(v2)
        # print(c)
        if s1.profile != s2.profile:
            macroDist = 10.0
        macroDist = sum(c) + len(s2.sequence) + len(s1.sequence) - 2 * len(c)
        nodeDist = 0.0
        for n1, n2 in zip(v1, v2):
            nC = NodeComparator(n1, n2)
            microDistance = nC.compareNodes(MicroDistance())
            nodeDist += microDistance
        #print("MACRO DIST= "+ str(macroDist))
        #print("micro DIST= "+ str(nodeDist))
        return self.alpha * macroDist + self.beta * nodeDist
