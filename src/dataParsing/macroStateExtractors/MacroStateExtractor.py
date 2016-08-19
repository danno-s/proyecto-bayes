#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from abc import ABCMeta, abstractmethod

from src.utils.sqlUtils import sqlWrapper
import src.utils as utils

class MacroStateExtractor:
    """
    Clase encargada de extraer los macro estados del sitio y almacenarlos en la base de datos.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        self.capture_table = utils.loadConfig.Config.getValue("capture_table")
        self.macroStatesL= self.loadMacroStates()

    @abstractmethod
    def loadMacroStates(self): pass

    def saveMacroStates(self):
        try:
            # Asigna las bases de datos que se accederan
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        # Limpia las tablas
        sqlPD.truncate("macrostates")

        sqlWrite = "INSERT INTO macrostates (macrostate, rule) VALUES ("  # Guardar contenido de macro estado.
        for macrostate in self.macroStatesL:
            sqlPD.write(sqlWrite + "'" + macrostate + "', '=');")


    @abstractmethod
    def map(self,url,urls):
        pass