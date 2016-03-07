from src.userempathetic.dataParsing.ExtractURLs import extractURLs
from src.userempathetic.dataParsing.ExtractUsers import extractUsers
from src.userempathetic.dataParsing.ExtractContentElements import extractContentElements
from src.userempathetic.dataParsing.dataParse import dataParse
from src.userempathetic.featureExtraction.calcLRSs import calcLRSs
from src.simulated.simulatedData.simulusers import *
from src.userempathetic.dataParsing.parseSessions import parseSessions
from src.userempathetic.featureExtraction.ExtractFeatures import extractFeatures, extractPostClusteringFeatures
from src.userempathetic.clustering.ExtractClusters import createClusterExtractor, userclustering, sessionclustering
import json


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


def simulate():
    print("\n\n...Generating data...\n\n")
    with open("simulatedData/simulConfig.json", "r") as f:
        file = f.read()
    generate(json.loads(file))


def extractFeats():
    print("...Extracting LRSs...\n")
    calcLRSs(simulation=True)
    print("...LRS extraction finished...\n")
    print("...Extracting Features...\n")
    extractFeatures(simulation=True)
    print("...Features extraction finished...\n")


if __name__ == '__main__':
    print("0 = dataParsing\n" +
          "1 = sessionParsing\n" +
          "2 = simulateData\n" +
          "3 = simulSessionParsing\n" +
          "4 = featureExtraction\n" +
          "5 = userClustering\n" +
          "6 = postUserClustering featureExtraction\n" +
          "7 = sessionClustering\n")
    a = int(input("Ingrese paso de inicio:"))
    if a <= 0:
        parseData()
    if a <= 1:
        print("...Parsing Sessions...\n")
        parseSessions(simulation=False)
        print("...Sessions parsing finished...\n")
    if a <= 2:
        print("...Simulating Data...\n")
        simulate()
    if a <= 3:
        parseSessions(simulation=True)
        print("...Simulation finished...\n")
    if a <= 4:
        sqlFT = sqlWrapper('FT')
        sqlFT.truncate('userfeatures')
        sqlFT.truncate('sessionfeatures')
        extractFeats()
    cE = createClusterExtractor()
    if a <= 5:
        print("\n\n...Performing users clustering...\n\n")
        userclustering(cE)
        print("\n\n User Clustering finished.\n\n")
    if a <= 6:
        print("...Extracting PostUserClustering Features...\n")
        extractPostClusteringFeatures(simulation=True)
        print("...PostUserClustering Features extraction finished...\n")
    if a <= 7:
        print("\n\n...Performing session clustering...\n\n")
        sessionclustering(cE)
        cE.visualizeClusters()
        print("\n\n Session Clustering finished.\n\n")

    print("\n\nUserEmpathetic process finished.\n\n")
