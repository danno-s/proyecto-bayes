from src.dataParsing.ExtractURLs import extractURLs
from src.dataParsing.ExtractUsers import extractUsers
from src.dataParsing.ExtractContentElements import extractContentElements
from src.dataParsing.parseSessions import parseSessions
from src.featureExtraction.calcLRSs import calcLRSs
from src.featureExtraction.calcUserLRSHistograms import calcUserLRSHistograms
from src.featureExtraction.extractUserClusteringFeatures import extractUserClusteringFeatures
from src.featureExtraction.linkSessionsWithLRSs import linkSessionsWithLRSs
from src.clustering.sessionClustering import sessionClustering
from src.simulatedData.ExtractSimlUsers import extractSimUsers
from src.simulatedData.parseSimulSession import parseSimulSession
from src.simulatedData.simulusers import *
from src.utils.loadConfig import Config

def parseData():
    extractURLs()
    print("...URL extraction finished...\n")
    extractUsers()
    print("...Users extraction finished...\n")
    extractContentElements()
    print("...Content elements extraction finished...\n")
    parseSessions()
    print("...Sessions extraction finished...\n")

def simulate():
    generate(1, 3)
    extractSimUsers()
    parseSimulSession()

def extractFeatures():
    calcLRSs()
    print("...LRS extraction finished...\n")
    extractUserClusteringFeatures()
    print("...User clustering features extraction finished...\n")
    calcUserLRSHistograms()
    print("...User-LRS Histograms calculations finished...\n")
    linkSessionsWithLRSs()
    print("...Sesssion-LRSs belongings table extraction finished...\n")


def clustering():
    sessionClustering()

if __name__ == '__main__':

    simulation = Config().getValue("simulate").lower() == "true"
    ## Modo normal

    if not simulation:
        parseData()
        print("\n\nData parsing finished.\n\n")
        extractFeatures()
        print("\n\nFeature Extraction finished.\n\n")
        clustering()
        print("\n\nClustering finished.\n\n")

        print("\n\nUserEmpathetic process finished.\n\n")

    ## Modo Simulado
    else:
        simulate()
        print("\n\nSimulated data Generation finished.\n\n")
        extractFeatures()
        print("\n\nFeature Extraction finished.\n\n")
        clustering()
        print("\n\nClustering finished.\n\n")

        print("\n\nUserEmpathetic process simulation finished.\n\n")
