#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Mapeador de los macro estados del sitio para los datos capturados.
"""
from abc import ABCMeta, abstractmethod
from src.dataParsing.MacroStateMapper import MacroStateMapper

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
        self.macroStatesD = self.loadMacroStates()
        self.macroStateRulesD = self.loadMacroStateRules()
        self.macroMapper = MacroStateMapper(self.macroStateRulesD)


    @abstractmethod
    def loadMacroStates(self): pass

    @abstractmethod
    def loadMacroStateRules(self): pass

    @abstractmethod
    def saveMacroStates(self): pass

    def getMacroMapper(self):
        return self.macroMapper