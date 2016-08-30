"""
Paso 7
Script para ejecucion del proceso de extraccion de LRSs.
"""
from src.featureExtraction.calcLRSs import calcLRSs
from src.executionSteps.main import start,finish


def lrsExtraction():
    start()
    calcLRSs()
    finish()
if __name__ == '__main__':
    lrsExtraction()
