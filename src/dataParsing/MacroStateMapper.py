import json
import re


class MacroStateMapper:
    """
    Clase encargada de mapear datos capturados desde base de datos "guidecapture" a sus Macro Estados
    correspondientes, segun una serie de reglas.
    """
    __instance = None

    def __new__(cls,rules):
        """ Constructor de MacroStateMapper que sigue patron de diseño Singleton para asignar una unica vez las reglas.

        Parameters
        ----------
        rules : dict
            un dict con los objetos MacroStateRule que representan las reglas de mapeo de macro estados.

        Returns
        -------
        """
        if MacroStateMapper.__instance is None:
            MacroStateMapper.__instance = object.__new__(cls)
            MacroStateMapper.__instance.rulesD = rules
        return MacroStateMapper.__instance

    def mapStrict(self, data):
        """ Mapeo de 'data' que retorna el MacroStateMap que representa el Macro Estado asociado al dato.
        En caso de no realizar el mapeo retorna False.

        Parameters
        ----------
        data : tuple
            (url, urls, variables) desde una fila de la tabla con datos de captura.

        Returns
        -------
        MacroStateMap
            Contiene reglas de mapeo, el ID del macro estado y su nombre.
        False
            Si no se encuentra un macro estado para el dato.

        """
        for macroStateRules in self.rulesD.values():
            result = self.evaluateMapping(macroStateRules)
            if result is not False:
                return result
        return False

    def map(self, data):
        """ Mapeo de 'data' que retorna el MacroStateMap que representa el Macro Estado asociado al dato.
        En caso de no realizar el mapeo retorna la url (data[0]).

        Parameters
        ----------
        data : tuple
            (url, urls, variables) desde una fila de la tabla con datos de captura.

        Returns
        -------
        MacroStateMap
            Contiene reglas de mapeo, el ID del macro estado y su nombre.
        str
            Si no se encuentra un macro estado para el dato retorna la url (data[0]).
        """
        for macroStateRules in self.rulesD.values():
            result = self.evaluateMapping(macroStateRules,data)
            if result is not False:
                return result
        return data[0]

    def evaluateMapping(self, macroStateRule, data):
        """ Evalua la regla 'macroStateRule' sobre el dato 'data'.

        Parameters
        ----------
        macroStateRule : MacroStateRule
        data : tuple
            (url, urls, variables) desde una fila de la tabla con datos de captura.

        Returns
        -------

        """
        ruleType = macroStateRule.getRuleType()
        varType = macroStateRule.getVarType()
        if data[0] is 'undefined':
            return False
        # Manejo por defecto del dato de entrada.
        info = data[0] #url

        # Manejo del dato de entrada en caso de que la regla se aplique para 'variables'
        if varType.startswith("variables"):
            pieces = varType.split(',')
            key = pieces[1]
            if data[2] is 'null':
                return False
            info = json.loads(data[2]) # variables
            if not info:
                return False
        # Manejo del dato de entrada en caso de que la regla se aplique para 'urljson'
        if varType == 'urljson':
            info = data[1] # urls
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

