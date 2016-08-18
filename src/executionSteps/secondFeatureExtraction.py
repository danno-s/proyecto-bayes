"""
Paso 10
Script para ejecucion de la segunda extraccion de features (que requier clustering de usuarios).
"""
from src.featureExtraction.ExtractFeatures import extractPostClusteringFeatures
from src.utils.sqlUtils import sqlWrapper


def secondFeatureExtraction():
    sqlFT = sqlWrapper('FT')
    sqlFT.truncate('sessionfeatures',
                   "feature_name = 'SessionUserClustersBelonging'")
    extractPostClusteringFeatures()

if __name__ == '__main__':
    secondFeatureExtraction()
