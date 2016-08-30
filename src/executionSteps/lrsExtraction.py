"""
Paso 7
Script para ejecucion del proceso de extraccion de LRSs.
"""
from src.featureExtraction.calcLRSs import calcLRSs


def lrsExtraction():
    from src.executionSteps.main import start, finish
    start()
    calcLRSs()
    finish()
if __name__ == '__main__':
    lrsExtraction()
