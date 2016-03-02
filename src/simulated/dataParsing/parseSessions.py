#!/usr/bin/python

"""
Extrae las distintas sesiones que existen en la base de datos
"""

from src.simulated.sessionParser.sessionizers.CompleteSessionizer import CompleteSessionizer
from src.simulated.sessionParser.sessionizers.EdgesSessionizer import EdgesSessionizer
from src.simulated.sessionParser.sessionizers.MacroCompleteSessionizer import MacroCompleteSessionizer
from src.simulated.sessionParser.sessionizers.MacroEdgesSessionizer import MacroEdgesSessionizer
from src.simulated.sessionParser.SessionParser import SessionParser
from src.userempathetic.utils.loadConfig import Config


def parseSessions():
    sessionizer_mode = Config().getValue("sessionizer_mode")
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

    sp = SessionParser(sessionizer)
    sp.parseSessions()
    sp.printSessions()


if __name__ == '__main__':
    parseSessions()
