# -*- coding: utf-8 -*-
"""
Paso 1
Script para ejecucion del proceso de extraccion de macro_ids.
"""
from src.dataParsing.ExtractURLs import extractURLs
from src.executionSteps.main import start,finish

def urlExtraction():
    start()
    extractURLs()
    finish()
if __name__ == '__main__':
    urlExtraction()
