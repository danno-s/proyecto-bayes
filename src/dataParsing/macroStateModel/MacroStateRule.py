class MacroStateRule:
    """
    Clase que modela una regla para mapear Macro Estados.
    """

    def __init__(self, _id, _arg, _ruleType, _varType, _weight=0):
        """ Constructor.

        Parameters
        ----------
        _id : int con ID de la regla
        _arg: str con argumento de la regla.
        _ruleType: str con tipo de regla ('exist', 'existAndEqual', 'equal', 'startsWith','regexp')
        _varType: str con tipo de variable del argumento ('url','urljson','variables, content_type')
        _weight: peso de la regla que define prioridad de aplicacion de la misma.

        Returns
        -------

        """
        self.id = _id
        self.arg = _arg
        self.ruleType = _ruleType
        self.varType = _varType
        self.weight = _weight
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
