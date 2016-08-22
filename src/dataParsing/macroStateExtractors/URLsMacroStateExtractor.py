# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from src.dataParsing.macroStateExtractors.MacroStateExtractor import MacroStateExtractor
from src.utils.sqlUtils import sqlWrapper


class URLsMacroStateExtractor(MacroStateExtractor):
    """
    Clase encargada de extraer los macro estados del sitio y almacenarlos en la base de datos.
    """
    def __init__(self):
        """Constructor

        Returns
        -------

        """
        MacroStateExtractor.__init__(self)

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
        sqlRead = 'SELECT DISTINCT urls from ' + self.capture_table
        rows = sqlGC.read(sqlRead)
        assert len(rows) > 0
        URLs = [x for x in rows]
        macrostates = [urlstree[0].replace(' ', '') for urlstree in URLs]
        return macrostates

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


