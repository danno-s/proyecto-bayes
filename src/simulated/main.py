from src.simulated.dataParsing.ExtractURLs import extractURLs
from src.simulated.dataParsing.ExtractUsers import extractUsers
from src.simulated.dataParsing.ExtractContentElements import extractContentElements
from src.simulated.dataParsing.dataParse import dataParse
from src.simulated.dataParsing.parseSessions import parseSessions as simulParseSession
from src.simulated.featureExtraction.calcLRSs import calcLRSs
from src.simulated.featureExtraction.ExtractFeatures import extractFeatures
from src.simulated.simulatedData.simulusers import *
from src.simulated.utils.loadConfig import Config
from src.userempathetic.dataParsing.parseSessions import parseSessions
from src.userempathetic.clustering.ExtractClusters import clustering

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
    generate(1)


def extractFeats():
    print("...Extracting LRSs...\n")
    calcLRSs()
    print("...LRS extraction finished...\n")
    print("...Extracting Features...\n")
    extractFeatures()
    print("...Features extraction finished...\n")

if __name__ == '__main__':
    print("0 = dataParsing\n"+
          "1 = sessionParsing\n"+
          "2 = simulateData\n"+
          "3 = simulSessionParsing\n"+
          "4 = featureExtraction\n"+
          "5 = clustering\n")
    a= int(input("Ingrese paso de inicio:"))
    if a <= 0:
        parseData()
    if a <= 1:
        print("...Parsing Sessions...\n")
        parseSessions()
        print("...Sessions parsing finished...\n")
    if a <= 2:
        print("...Simulating Data...\n")
        simulate()
    if a <= 3:
        simulParseSession()
        print("...Simulation finished...\n")
    if a <= 4:
        extractFeats()
    if a <= 5:
        print("\n\n...Performing session clustering...\n\n")
        clustering()
        print("\n\nClustering finished.\n\n")

    print("\n\nUserEmpathetic process finished.\n\n")
