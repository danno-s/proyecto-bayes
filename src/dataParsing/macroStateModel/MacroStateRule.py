class MacroStateRule:

    def __init__(self,id,arg,ruleType,varType,weight):
        self.id = id
        self.arg = arg
        self.ruleType = ruleType
        self.varType = varType
        self.weight = weight
        self.macrostatemap = None

    def getId(self):
        return self.id

    def setArg(self,arg):
        self.arg = arg

    def getArg(self):
        return self.arg

    def setRuleType(self,ruleType):
        self.ruleType = ruleType

    def getRuleType(self):
        return self.ruleType

    def setVarType(self,varType):
        self.varType = varType

    def getVarType(self):
        return self.varType

    def setWeight(self,weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setMacrostatemap(self, macrostatemap):
        self.macrostatemap = macrostatemap

    def getMacrostatemap(self):
        return self.macrostatemap

    def __str__(self):
        return 'Rule {0}: {1} {2} {3} -> {4}'.format(str(self.id),
                                               str(self.varType),
                                               str(self.ruleType),
                                               str(self.arg),
                                               self.macrostatemap)
