from src.sessionParser.sessionizers.Sessionizer import Sessionizer


class MacroEdgesSessionizer(Sessionizer):
    """
    Sessionizer que considera solo los pasos de "borde" para cada macro estado para formar una sesion.

    Esto es, dado una parte de la secuencia en que se repiten los macro IDs, considerara unicamente el primero
    y el ultimo.

    Guarda unicamente el macro estado de cada paso en la sesion.
    """

    def __init__(self):
        Sessionizer.__init__(self)

    def bufferAccepts(self, sb, prevStep, step):
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
        """Retorna la tupla unicamente con el macro ID.

        Parameters
        ----------
        macro_id
        micro_id

        Returns
        -------
        (int, None)
        """
        return (macro_id, None)
