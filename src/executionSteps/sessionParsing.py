# -*- coding: utf-8 -*-

"""
Paso 5
Script para ejecucion del proceso de extraccion de Sesiones.
"""
from src.dataParsing.parseSessions import parseSessions


def sessionParsing():
    from src.executionSteps.main import start, finish
    start()
    parseSessions()
    finish()
if __name__ == '__main__':
    sessionParsing()
