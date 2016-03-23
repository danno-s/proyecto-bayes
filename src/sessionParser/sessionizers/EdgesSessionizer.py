from src.sessionParser.sessionizers.Sessionizer import Sessionizer


class EdgesSessionizer(Sessionizer):
    """
    Sessionizer que considera sólo los pasos de "borde" para cada macro estado para formar una sesión.

    Esto es, dado una parte de la secuencia en que se repiten los macro IDs, considerará únicamente el primero
    y el último.

    Además, en la sesión guarda los micro estados de estos pasos.
    """
    def __init__(self):
        Sessionizer.__init__(self)

    def bufferAccepts(self, sb, prevStep, step):  # TODO: (args, vals)
        """Acepta el paso actual cuando es el principio de una secuencia o cuando es un borde de una subsecuencia de
        macro_ids iguales consecutivas.

        Parameters
        ----------
        sb
        prevStep
        step

        Returns
        -------
        bool
            True si es borde o comienzo de secuencia. False si no.
        """
        if sb.isEmpty():
            return True
        if prevStep[1] == step[1] and sb.last()[0] == prevStep[1]:
            return False
        else:
            return True

    def toIDPair(self, macro_id, micro_id):
        """Retorna la tupla con ambos IDs.

        Parameters
        ----------
        macro_id
        micro_id

        Returns
        -------
        (int, int)
        """
        return (macro_id, micro_id)
