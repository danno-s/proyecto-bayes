#!/usr/bin/python

"""
Extrae las distintas sesiones que existen en la base de datos
"""

from src.sessionParser.sessionizers.CompleteSessionizer import CompleteSessionizer
from src.sessionParser.sessionizers.EdgesSessionizer import EdgesSessionizer
from src.sessionParser.sessionizers.MacroEdgesSessionizer import MacroEdgesSessionizer
from src.sessionParser.sessionizers.MacroCompleteSessionizer import MacroCompleteSessionizer
from src.sessionParser.SessionParser import SessionParser
from src.utils.loadConfig import Config


def parseSessions(simulation=False):
    """ Extrae sesiones dependiendo de los sessionizers definidos en el archivo de configuración del sistema.

    Parameters
    ----------
    simulation : bool
        Modo de ejecución.

    Returns
    -------

    """
    sessionizer_mode = Config.getValue("sessionizer_mode")
    if sessionizer_mode == "MacroComplete":
        sessionizer = MacroCompleteSessionizer()
    elif sessionizer_mode == "Complete":
        sessionizer = CompleteSessionizer()
    elif sessionizer_mode == "MacroEdges":
        sessionizer = MacroEdgesSessionizer()
    elif sessionizer_mode == "Edges":
        sessionizer = EdgesSessionizer()
    else:
        raise Exception  # TODO: crear configuration exception.

    sp = SessionParser(sessionizer, simulation=simulation)
    sp.parseSessions()
    sp.printSessions()


if __name__ == '__main__':
    parseSessions()
