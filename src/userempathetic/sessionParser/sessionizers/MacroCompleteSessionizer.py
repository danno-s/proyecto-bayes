from src.userempathetic.sessionParser.sessionizers.Sessionizer import Sessionizer


class MacroCompleteSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)
        pass

    def bufferAccepts(self, sb, prevStep, step):
        return True

    def toIDPair(self, macro_id, micro_id):
        return (macro_id, None)
