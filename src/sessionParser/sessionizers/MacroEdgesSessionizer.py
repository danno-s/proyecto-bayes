from src.sessionParser.sessionizers.Sessionizer import Sessionizer


class MacroEdgesSessionizer(Sessionizer):

    def __init__(self):
        Sessionizer.__init__(self)

    def bufferAccepts(self, sb, prevStep, step):    #TODO: (args, vals)
        if sb.isEmpty():
            return True
        if prevStep[1] == step[1] and sb.last()[0]==prevStep[1]:
            return False
        else:
            return True

    def toIDPair(self, macro_id, micro_id):
        return (macro_id,None)
