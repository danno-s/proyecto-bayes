#!/usr/bin/python

"""
Extrae las distintas sesiones que existen en la base de datos
"""

from src.sessionParser.sessionizers.CompleteSessionizer import CompleteSessionizer
from src.sessionParser.sessionizers.EdgesSessionizer import EdgesSessionizer
from src.sessionParser.sessionizers.MacroCompleteSessionizer import MacroCompleteSessionizer
from src.sessionParser.sessionizers.MacroEdgesSessionizer import MacroEdgesSessionizer
from src.sessionParser.SessionParser import SessionParser


def parseSessions():

    a = SessionParser(EdgesSessionizer())
    a.parseSessions()
    a.printSessions()

if __name__ == '__main__':
    parseSessions()