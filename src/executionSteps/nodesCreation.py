# -*- coding: utf-8 -*-

"""
Paso 4
Script para ejecucion del proceso de creacion de nodos.
"""
from src.dataParsing.dataParse import dataParse
from src.executionSteps.main import start,finish


def nodesCreation():
    start()
    dataParse()
    finish()
if __name__ == '__main__':
    nodesCreation()
