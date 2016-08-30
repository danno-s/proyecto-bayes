# -*- coding: utf-8 -*-

"""
Paso 3
Script para ejecucion del proceso de extraccion de content elements.
"""
from src.dataParsing.ExtractContentElements import extractContentElements

def contentElementsExtraction():
    from src.executionSteps.main import start, finish
    start()
    extractContentElements()
    finish()
if __name__ == '__main__':
    contentElementsExtraction()
