# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from src.dataParsing.macroStateExtractors.MacroStateExtractor import MacroStateExtractor
from src.dataParsing.macroStateModel.MacroStateRule import MacroStateRule
from src.dataParsing.macroStateModel.MacroStateMap import MacroStateMap
from src.dataParsing.MacroStateMapper import MacroStateMapper

from src.utils.sqlUtils import sqlWrapper


class URLsMacroStateExtractor(MacroStateExtractor):
    """
    Clase encargada de extraer los macro estados del sitio y almacenarlos en la base de datos.
    """
    __instance = None
    def __new__(cls):
        """ Constructor para obtener unica instancia (Singleton Pattern)
        Returns
        -------

        """
        if URLsMacroStateExtractor.__instance is None:
            URLsMacroStateExtractor.__instance = object.__new__(cls)
            URLsMacroStateExtractor.__instance.urlsL = URLsMacroStateExtractor.__instance.__loadURLs()
            URLsMacroStateExtractor.__instance.argsD = URLsMacroStateExtractor.__instance.__loadArgs()
            URLsMacroStateExtractor.__instance.macroStatesD = URLsMacroStateExtractor.__instance.loadMacroStates()
            URLsMacroStateExtractor.__instance.macroStateRulesD = URLsMacroStateExtractor.__instance.loadMacroStateRules()
            URLsMacroStateExtractor.__instance.macroMapper = MacroStateMapper(URLsMacroStateExtractor.__instance.macroStateRulesD)

        return URLsMacroStateExtractor.__instance

    def __loadURLs(self):
        """Carga lista con todos los arboles de URLs unicos.

        Returns
        -------
        """
        try:
            # Asigna la base de datos que se accedera
            sqlGC = sqlWrapper(db='GC')
        except:
            raise
        from src.utils.loadConfig import Config
        capture_table = Config.getValue("capture_table")
        sqlRead = 'SELECT DISTINCT urls from ' + capture_table
        rows = sqlGC.read(sqlRead)
        assert len(rows) > 0
        URLs = [x for x in rows]
        return [urlstree[0].replace(' ', '') for urlstree in URLs]

    def loadMacroStates(self):
        macroStatesD = dict()
        for i in range(len(self.urlsL)):
            msMap = MacroStateMap(i+1, "S"+str(i+1))
            macroStatesD[i+1] = msMap
        return macroStatesD

    def __loadArgs(self):
        argsD = dict()
        for i,urlstree in enumerate(self.urlsL):
            argsD[i+1] = urlstree.replace(' ', '')
        return argsD

    def loadMacroStateRules(self):
        rulesD = dict()
        for i in self.macroStatesD.keys():
            msRule = MacroStateRule(_id=i, _arg=self.argsD[i],_ruleType= 'equal',_varType='urljson',_weight=1)
            self.macroStatesD[i].addRule(msRule)
            rulesD[i]= msRule
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
            macroMapper = MacroStateMapper(URLsMacroStateExtractor.__instance.macroStateRulesD)
            URLsMacroStateExtractor.__instance.macroMapper = macroMapper
            return macroMapper

if __name__ == '__main__':

    from src.utils.sqlUtils import sqlWrapper

    umse = URLsMacroStateExtractor()

    umse.saveMacroStates()