# -*- coding: utf-8 -*-
"""
Paso 1
Script para ejecucion del proceso de extraccion de MacroEstados.
"""
from src.dataParsing.ExtractMacroStates import extractMacroStates


def macroStatesExtraction():
    from src.executionSteps.main import start, finish
    start()
    extractMacroStates()
    finish()

if __name__ == '__main__':
    macroStateExtraction()
