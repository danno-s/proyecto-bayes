

class MacroStateMap:

    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.rules = list()

    def setRules(self,rules):
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

