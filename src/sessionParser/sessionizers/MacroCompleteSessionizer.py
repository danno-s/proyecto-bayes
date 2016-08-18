from src.sessionParser.sessionizers.Sessionizer import Sessionizer


class MacroCompleteSessionizer(Sessionizer):
    """
    Sessionizer que considera todos los pasos capturados para formar una sesion, pero guarda solo los macro estados.
    """

    def __init__(self):
        Sessionizer.__init__(self)
        pass

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
