# -*- coding: utf-8 -*-

"""
Paso 2
Script para ejecucion del proceso de extraccion de usuarios.
"""
from src.dataParsing.ExtractUsers import extractUsers
from src.executionSteps.main import start,finish


def userExtraction():
    start()
    extractUsers()
    finish()
if __name__ == '__main__':
    userExtraction()
