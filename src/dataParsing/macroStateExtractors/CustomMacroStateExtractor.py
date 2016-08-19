# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from src.dataParsing.macroStateExtractors.MacroStateExtractor import MacroStateExtractor


class CustomMacroStateExtractor(MacroStateExtractor):
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
        return ['{"regexp":"(http://)?(www.)?nosfuimos.cl/search-ride*"}']#,
                            #('Viaje','{"variables":"viaje3"}')]

    def map(self, url, urls):
        #busca en tabla macrostate la macro_id para los datos url, urls....
        # en este caso debiera buscar por la re que haga match con url
        return 1
