# -*- coding: utf-8 -*-

"""
Paso 4
Script para ejecucion del proceso de creacion de nodos.
"""
from src.dataParsing.dataParse import dataParse


def nodesCreation():
    from src.executionSteps.main import start, finish
    start()
    dataParse()
    finish()
if __name__ == '__main__':
    nodesCreation()
