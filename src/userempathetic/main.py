from src.userempathetic.dataParsing.ExtractURLs import extractURLs
from src.userempathetic.dataParsing.ExtractUsers import extractUsers
from src.userempathetic.dataParsing.ExtractContentElements import extractContentElements
from src.userempathetic.dataParsing.dataParse import dataParse
from src.userempathetic.dataParsing.parseSessions import parseSessions
from src.userempathetic.featureExtraction.calcLRSs import calcLRSs
from src.userempathetic.featureExtraction.ExtractFeatures import extractFeatures, extractPostClusteringFeatures
from src.userempathetic.clustering.ExtractClusters import createClusterExtractor, userclustering, sessionclustering


def parseData():
    print("...Extracting URLs...\n")
    extractURLs()
    print("...URLs extraction finished...\n")
    print("...Extracting Users...\n")
    extractUsers()
    print("...Users extraction finished...\n")
    print("...Extracting Content Elements...\n")
    extractContentElements()
    print("...Content elements extraction finished...\n")

    print("...Parsing Data...\n")
    dataParse()
    print("...Data parsing finished...\n")


def extractFeats():
    print("...Extracting LRSs...\n")
    calcLRSs()
    print("...LRS extraction finished...\n")
    print("...Extracting Features...\n")
    extractFeatures()
    print("...Features extraction finished...\n")


if __name__ == '__main__':
    print("0 = dataParsing\n" +
          "1 = sessionParsing\n" +
          "2 = featureExtraction\n" +
          "3 = userClustering\n" +
          "4 = postUserClustering featureExtraction\n" +
          "5 = sessionClustering\n")
    a = int(input("Ingrese paso de inicio:"))
    if a <= 0:
        parseData()
    if a <= 1:
        print("...Parsing Sessions...\n")
        parseSessions()
        print("...Sessions parsing finished...\n")
    if a <= 2:
        extractFeats()
    cE = createClusterExtractor()
    if a <= 3:
        print("\n\n...Performing users clustering...\n\n")
        userclustering(cE)
        print("\n\n User Clustering finished.\n\n")
    if a <= 4:
        print("...Extracting PostUserClustering Features...\n")
        extractPostClusteringFeatures()
        print("...PostUserClustering Features extraction finished...\n")
    if a <= 5:
        print("\n\n...Performing session clustering...\n\n")
        sessionclustering(cE)
        cE.visualizeClusters()
        print("\n\n Session Clustering finished.\n\n")

    print("\n\nUserEmpathetic process finished.\n\n")
