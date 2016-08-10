from src.sessionParser.sessionizers.Sessionizer import Sessionizer


class CompleteSessionizer(Sessionizer):
    """
    Sessionizer que considera todos los pasos capturados para formar una sesion.
    """

    def __init__(self):
        Sessionizer.__init__(self)

    def bufferAccepts(self, sb, prevStep, step):
        """Siempre acepta el paso actual.
        Parameters
        ----------
        sb
        prevStep
        step

        Returns
        -------
        bool
            True.
        """
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
