from src.dataParsing.ExtractURLs import extractURLs
from src.dataParsing.ExtractUsers import extractUsers
from src.dataParsing.parseSessions import parseSessions
from src.featureExtraction.calcLRSs import calcLRSs
from src.featureExtraction.extractUserClusteringFeatures import extractUserClusteringFeatures
from src.featureExtraction.calcUserLRSHistograms import calcUserLRSHistograms
from src.featureExtraction.linkSessionsWithLRSs import linkSessionsWithLRSs
from src.clustering.sessionClustering import sessionClustering


def parseData():
    extractURLs()
    extractUsers()
    parseSessions()


def extractFeatures():
    calcLRSs()
    extractUserClusteringFeatures()
    calcUserLRSHistograms()
    linkSessionsWithLRSs()

def clustering():
    sessionClustering()

if __name__ == '__main__':
    parseData()
    print("\n\nData parsing finished.\n\n")
    extractFeatures()
    print("\n\nFeature Extraction finished.\n\n")
    clustering()
    print("\n\nClustering finished.\n\n")

    print("\n\nUserEmpathetic process finished.\n\n")