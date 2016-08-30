# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from src.dataParsing.macroStateExtractors.MacroStateExtractor import MacroStateExtractor
from src.dataParsing.macroStateModel.MacroStateMap import MacroStateMap
from src.dataParsing.macroStateModel.MacroStateRule import MacroStateRule
from src.utils.sqlUtils import sqlWrapper
from src.dataParsing.MacroStateMapper import MacroStateMapper


class CustomMacroStateExtractor(MacroStateExtractor):
    """
    Clase encargada de extraer los macro estados del sitio y almacenarlos en la base de datos.
    """
    __instance = None
    def __new__(cls):
        """ Constructor para obtener unica instancia (Singleton Pattern)
        Returns
        -------

        """
        if CustomMacroStateExtractor.__instance is None:
            CustomMacroStateExtractor.__instance = object.__new__(cls)
            CustomMacroStateExtractor.__instance.macroStatesD = CustomMacroStateExtractor.__instance.loadMacroStates()
            CustomMacroStateExtractor.__instance.macroStateRulesD = CustomMacroStateExtractor.__instance.loadMacroStateRules()
            CustomMacroStateExtractor.__instance.macroMapper = CustomMacroStateExtractor.__instance.getMacroMapper()

        return CustomMacroStateExtractor.__instance

    def loadMacroStates(self):
        """Carga Macro estados predefinidos a la tabla macrostates.

        Returns
        -------
        """
        try:
            # Asigna las bases de datos que se accederan
            sqlGC = sqlWrapper(db='GC')
        except:
            raise
        sqlRead = "SELECT id,name from macrostatemap"
        rows = sqlGC.read(sqlRead)
        assert len(rows) > 0
        macroStatesD = dict()
        for row in rows:
            msMap = MacroStateMap(row[0], row[1])
            macroStatesD[row[0]] = msMap
        return macroStatesD

    def loadMacroStateRules(self):
        try:
            sqlGC = sqlWrapper(db='GC')
        except:
            raise
        sqlRead = "SELECT id,macrostatemap_id,arg,type,weight,var_type from macrostaterule"
        rows = sqlGC.read(sqlRead)
        assert len(rows) > 0
        rulesD = dict()
        for row in rows:
            msRule = MacroStateRule(_id=row[0],_arg=row[2],_ruleType=row[3],_weight=row[5],_varType=row[4])
            self.macroStatesD[row[1]].addRule(msRule)
            rulesD[row[0]]=msRule
        return rulesD

    def saveMacroStates(self):
        """
        Almacena las reglas y macro estados extraidos en la base de datos "parseddata".
        Returns
        -------

        """
        try:
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlPD.truncateRestricted("macrostaterule")
        sqlPD.truncateRestricted("macrostatemap")

        sqlWrite = "INSERT INTO macrostatemap (id,name) VALUES (%s,%s)"
        writeL = [(x,y.getName()) for x,y in self.macroStatesD.items()]
        sqlPD.writeMany(sqlWrite,writeL)

        sqlWrite = "INSERT INTO macrostaterule (id,macrostatemap_id,arg,type,weight,var_type) VALUES (%s,%s,%s,%s,%s,%s)"
        writeL = [(x.getId(),x.getMacrostatemap().getId(), x.getArg(),x.getRuleType(),x.getWeight(),x.getVarType()) for x in self.macroStateRulesD.values()]
        sqlPD.writeMany(sqlWrite, writeL)

    def getMacroMapper(self):
        """
        Retorna el MacroStateMapper utilizado para mapear los macro estados. En caso de no haber sido instanciado,
        se construye usando el diccionario de reglas cargado desde la base de datos.
        Returns
        -------

        """
        try:
            return self.macroMapper
        except AttributeError:
            macroMapper = MacroStateMapper(CustomMacroStateExtractor.__instance.macroStateRulesD)
            CustomMacroStateExtractor.__instance.macroMapper = macroMapper
            return macroMapper


