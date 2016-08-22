# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from src.dataParsing.macroStateExtractors.MacroStateExtractor import MacroStateExtractor
from src.dataParsing.macroStateModel import MacroStateMap


class CustomMacroStateExtractor(MacroStateExtractor):
    """
    Clase encargada de extraer los macro estados del sitio y almacenarlos en la base de datos.
    """
    def __init__(self):
        """Constructor

        Returns
        -------

        """
        self.macroStatesD= self.__loadMacroStatesD()
        MacroStateExtractor.__init__(self)

    def __loadMacroStatesD(self):
        """Carga Macro estados predefinidos a la tabla macrostates.

                Returns
                -------

                """
        try:
            # Asigna las bases de datos que se accederan
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "SELECT id,name from macrostatemap"
        rows = sqlPD.read(sqlRead)
        assert len(rows) > 0
        macroStatesD = dict()
        for row in rows:
            msMap = MacroStateMap(row[0], row[1])
            macroStatesD[row[0]] = msMap
        return macroStatesD

    def loadMacroStates(self):
        """Carga Macro estados predefinidos a la tabla macrostates.

        Returns
        -------

        """
        return list(self.macroStatesD.keys())

    def map(self, data):
        """
        Obtiene el id en la base de datos del macro estado

        Parameters
        ----------
        data: (url,urls,variables)
            La url principal a buscar, el arbol de urls a buscar y las variables de la captura.
        Returns
        -------
        int
            La id del macro estado.
        """

        #busca en tabla macrostate la macro_id para los datos url, urls....
        # en este caso debiera buscar por la re que haga match con url
        import re
        import json
        macro_id = -1
        for i, macroState in enumerate(self.macroStatesL):
            ruleJSON = json.loads(macroState)
            p = re.compile(ruleJSON["regex"])
            m = p.match(data[0])
            if m:
                macro_id = i
                break
                
        print(data[0])
        print("macro_id = " + str(i))


if __name__ == '__main__':
    from src.utils.sqlUtils import sqlWrapper

    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    cmse = CustomMacroStateExtractor()
    #rows = sqlPD.read("SELECT url FROM url")
    #for row in rows:
    #    cmse.map(row[0],None)
    cmse.saveMacroStates()
    rows = sqlPD.read("SELECT * FROM macrostates")
    for row in rows:
        print(row)
