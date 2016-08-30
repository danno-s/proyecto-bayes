"""
Paso 8
Script para ejecucion de la primera extraccion de features.
"""
from src.featureExtraction.ExtractFeatures import extractFeatures
from src.utils.sqlUtils import sqlWrapper
from src.executionSteps.main import start,finish


def firstFeatureExtraction():
    start()
    sqlFT = sqlWrapper('FT')
    sqlFT.truncateRestricted('userfeatures')
    sqlFT.truncateRestricted('sessionfeatures')
    extractFeatures()
    finish()

if __name__ == '__main__':
    firstFeatureExtraction()
