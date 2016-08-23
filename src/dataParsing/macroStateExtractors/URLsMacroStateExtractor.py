# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from src.dataParsing.macroStateExtractors.MacroStateExtractor import MacroStateExtractor
from src.dataParsing.macroStateModel.MacroStateRule import MacroStateRule
from src.dataParsing.macroStateModel.MacroStateMap import MacroStateMap

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
            MacroStateExtractor.__init__(URLsMacroStateExtractor.__instance)

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
            msRule = MacroStateRule(i, self.argsD[i], 'equal','urljson',1)
            self.macroStatesD[i].addRule(msRule)
            rulesD[i]= msRule
        return rulesD

    def saveMacroStates(self):
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


    def map(self, data):
        """
        Obtiene el id en la base de datos de un arbol de urls

        Parameters
        ----------
        data: (url,urls,variables)
            La url principal a buscar, el arbol de urls a buscar y las variables de la captura.
        Returns
        -------
        int
            El id del arbol de urls
        """
        try:
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "select id from macrostates where macrostate = '" + data[1] + "'"
        rows = sqlPD.read(sqlRead)
        return str(rows[0][0])

if __name__ == '__main__':

    from src.utils.sqlUtils import sqlWrapper

    umse = URLsMacroStateExtractor()

    umse.saveMacroStates()