

class MacroStateMap:
    """
    Clase que modela una Macro Estado conocido (puede ser mapeado).
    """

    def __init__(self,_id,_name):
        """

        Parameters
        ----------
        _id : int
            ID del macro estado.
        _name: str
            Nombre del macro estado.

        Returns
        -------

        """
        self.id = _id
        self.name = _name
        self.rules = list()

    def setRules(self,rules):
        """

        Parameters
        ----------
        rules : list
            Lista de MacroStateRule .

        Returns
        -------

        """
        self.rules = rules

    def getRules(self):
        return self.rules

    def addRule(self,rule):
        self.rules.append(rule)
        rule.setMacrostatemap(self)

    def removeRule(self,rule):
        self.rules.remove(rule)

    def getId(self):
        return self.id

    def getRuleType(self):
        return self.ruleType

    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name


    def __str__(self):
        return self.name

