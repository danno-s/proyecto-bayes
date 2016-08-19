# -*- coding: utf-8 -*-

from src.utils.sqlUtils import sqlWrapper
from src.utils.loadConfig import Config
from src.dataParsing.macroStateExtractors.URLsMacroStateExtractor import URLsMacroStateExtractor
from src.dataParsing.macroStateExtractors.CustomMacroStateExtractor import CustomMacroStateExtractor

macroStateExtractorsD = {"URLs": URLsMacroStateExtractor,
                         "Custom": CustomMacroStateExtractor}


def extractMacroStates():
    """Extrae MacroEstados del sitio, dependiendo del MacroStateExtractor escogido en archivo de configuracion.

    Returns
    -------
    """
    mse = Config.getValue("macrostate_extractor")
    '''
    if mse == 'URLs':
        macrostateE = URLsMacroStateExtractor()
    elif mse == 'Custom':
        macrostateE = CustomMacroStateExtractor()
    else:
        print("Error iniciando MacroStateExtractor")
        return
    '''
    macrostateE = macroStateExtractorsD[mse]()
    macrostateE.saveMacroStates()


if __name__ == '__main__':
    extractMacroStates()
