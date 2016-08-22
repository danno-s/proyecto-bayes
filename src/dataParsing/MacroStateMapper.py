import json
import re

from src.dataParsing.macroStateModel import MacroStateRule
from src.utils.sqlUtils import sqlWrapper


class MacroStateMapper:
    __instance = None

    def __new__(cls):
        if MacroStateMapper.__instance is None:
            MacroStateMapper.__instance = object.__new__(cls)
            MacroStateMapper.__instance.rules = MacroStateMapper.__instance.__getRules()
        return MacroStateMapper.__instance

    def __getRules(self):
        try:
            # Asigna las bases de datos que se accederan
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "SELECT id,macrostatemap_id,arg,type,weight,var_type from macrostaterule"
        rows = sqlPD.read(sqlRead)
        assert len(rows) > 0
        L = []
        from src.utils.dataParsingUtils import getMacroStateMap
        for row in rows:
            msRule = MacroStateRule(row[0],row[2],row[3],row[5],row[4])
            msMap = getMacroStateMap(row[1])
            msMap.addRule(msRule)
            L.append(msRule)
        return L

    def mapStrict(self, data):
        for macroStateRules in self.rules:
            result = self.evaluateMapping(macroStateRules)
            if result is not False:
                return result
        return False

    def map(self, data):
        for macroStateRules in self.rules:
            result = self.evaluateMapping(macroStateRules,data)
            if result is not False:
                return result
        return data[0]

    def evaluateMapping(self, macroStateRule, data):
        ruleType = macroStateRule.getRuleType()
        varType = macroStateRule.getVarType()
        if data[0] is 'undefined':
            return False
        info = data[0] #url

        if varType.startswith("variables"):
            pieces = varType.split(',')
            key = pieces[1]
            if data[2] is 'null':
                return False
            info = json.loads(data[2]) # variables
            if not info:
                return False

        if ruleType == 'equal':
            return self.evaluateMappingEqual(macroStateRule, info)

        elif ruleType == 'startsWith':
            return self.evaluateMappingStartsWith(macroStateRule, info)

        elif ruleType == 'regexp':
            return self.evaluateMappingRegexp(macroStateRule, info)

        elif ruleType == 'exists':
            return self.evaluateMappingExists(macroStateRule, key, info)

        elif ruleType == 'existsAndEqual':
            return self.evaluateMappingExistsAndEqual(macroStateRule, key, info)

        return False

    def evaluateMappingExists(self,macroStateRule, key, info):
        if key in info.keys():
            return macroStateRule.getMacrostatemap()
        return False

    def evaluateMappingExistsAndEqual(self,macroStateRule, key, info):
        if key in info.keys():
            val = info[key]
            arg = macroStateRule.getArg()
            if val == arg:
                return macroStateRule.getMacrostatemap()
        return False

    def evaluateMappingEqual(self,macroStateRule, info):
       if macroStateRule.getArg() == info:
           return macroStateRule.getMacrostatemap()
       return False

    def evaluateMappingStartsWith(self,macroStateRule, info):
        result = info.startswith(macroStateRule.getArg())
        if result is True:
            return macroStateRule.getMacrostatemap()
        return False

    def evaluateMappingRegexp(self,macroStateRule, info):
        pattern = re.compile(macroStateRule.getArg())
        m = pattern.match(info)
        if m:
            return macroStateRule.getMacrostatemap()
        return False

