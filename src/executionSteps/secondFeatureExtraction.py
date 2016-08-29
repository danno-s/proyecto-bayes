"""
Paso 10
Script para ejecucion de la segunda extraccion de features (que requier clustering de usuarios).
"""
from src.featureExtraction.ExtractFeatures import extractPostClusteringFeatures
from src.utils.sqlUtils import sqlWrapper
from src.executionSteps.main import start,finish


def secondFeatureExtraction():
    start()
    sqlFT = sqlWrapper('FT')
    sqlFT.truncate('sessionfeatures',
                   "feature_name = 'SessionUserClustersBelonging'")
    extractPostClusteringFeatures()
    finish()
if __name__ == '__main__':
    secondFeatureExtraction()
