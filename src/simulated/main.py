from src.userempathetic.dataParsing.ExtractURLs import extractURLs
from src.userempathetic.dataParsing.ExtractUsers import extractUsers
from src.userempathetic.dataParsing.ExtractContentElements import extractContentElements
from src.userempathetic.dataParsing.dataParse import dataParse
from src.userempathetic.dataParsing.parseSessions import parseSessions
from src.userempathetic.featureExtraction.calcLRSs import calcLRSs
from src.userempathetic.featureExtraction.ExtractFeatures import extractFeatures
from src.userempathetic.clustering.sessionClustering import sessionClustering
from src.userempathetic.simulatedData.simulusers import *
from src.userempathetic.utils.loadConfig import Config

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
    sessionClustering()

if __name__ == '__main__':

    simulation = Config().getValue("simulate").lower() == "true"
    ## Modo normal

    if not simulation:
        parseData()
        print("...Parsing Sessions...\n")
        parseSessions()
        print("...Sessions parsing finished...\n")
        extractFeats()
        clustering()
        print("\n\nClustering finished.\n\n")

        print("\n\nUserEmpathetic process finished.\n\n")

    ## Modo Simulado
    else:
        simulate()
        print("\n\nSimulated data and sessions generation finished.\n\n")
        extractFeats()
        print("\n\nFeature Extraction finished.\n\n")
        clustering()
        print("\n\nClustering finished.\n\n")

        print("\n\nUserEmpathetic process simulation finished.\n\n")
