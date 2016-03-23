from src.featureExtraction.ExtractFeatures import extractFeatures
from src.utils.sqlUtils import sqlWrapper

def firstFeatureExtraction():
    sqlFT = sqlWrapper('FT')
    sqlFT.truncate('userfeatures')
    sqlFT.truncate('sessionfeatures')
    extractFeatures()

if __name__ == '__main__':
    firstFeatureExtraction()
