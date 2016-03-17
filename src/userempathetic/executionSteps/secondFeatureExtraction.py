from src.userempathetic.featureExtraction.ExtractFeatures import extractPostClusteringFeatures
from src.userempathetic.utils.sqlUtils import sqlWrapper


def secondFeatureExtraction():
    sqlFT = sqlWrapper('FT')
    sqlFT.truncate('sessionfeatures',"feature_name = 'SessionUserClustersBelonging'")
    extractPostClusteringFeatures()

if __name__ == '__main__':
    secondFeatureExtraction()
