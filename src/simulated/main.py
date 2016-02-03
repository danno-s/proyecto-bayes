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

def clustering():
    print("\n\n...Performing clustering...\n\n")
    # sessionClustering()

if __name__ == '__main__':

    simulation = Config().getValue("simulate").lower() == "true"
    ## Modo normal

    parseData()
    print("...Parsing Sessions...\n")
    parseSessions()
    print("...Sessions parsing finished...\n")
    simulate()
    simulParseSession()
    print("\n\nSimulated data and sessions generation finished.\n\n")
    extractFeats()
    print("\n\nFeature Extraction finished.\n\n")
    clustering()
    print("\n\nClustering finished.\n\n")

    print("\n\nsimulated process simulation finished.\n\n")
