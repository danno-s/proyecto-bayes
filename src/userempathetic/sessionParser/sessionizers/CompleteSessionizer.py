from src.userempathetic.sessionParser.sessionizers.Sessionizer import Sessionizer


class CompleteSessionizer(Sessionizer):
    def __init__(self):
        Sessionizer.__init__(self)

    def bufferAccepts(self, sb, prevStep, step):  # TODO: (args, vals)
        return True

    def toIDPair(self, macro_id, micro_id):
        return (macro_id, micro_id)
