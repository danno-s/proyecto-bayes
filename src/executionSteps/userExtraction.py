# -*- coding: utf-8 -*-

"""
Paso 2
Script para ejecucion del proceso de extraccion de usuarios.
"""
from src.dataParsing.ExtractUsers import extractUsers


def userExtraction():
    from src.executionSteps.main import start, finish
    start()
    extractUsers()
    finish()
if __name__ == '__main__':
    userExtraction()
