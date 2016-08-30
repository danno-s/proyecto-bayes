#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Extractor de los macro estados del sitio.
"""
from abc import ABCMeta, abstractmethod


class MacroStateExtractor:
    """
    Clase encargada de extraer los macro estados del sitio y almacenarlos en la base de datos.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def loadMacroStates(self): pass

    @abstractmethod
    def loadMacroStateRules(self): pass

    @abstractmethod
    def saveMacroStates(self): pass

    @abstractmethod
    def getMacroMapper(self): pass
