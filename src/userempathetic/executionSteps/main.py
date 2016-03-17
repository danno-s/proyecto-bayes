from src.userempathetic.executionSteps.urlExtraction import urlExtraction
from src.userempathetic.executionSteps.userExtraction import userExtraction
from src.userempathetic.executionSteps.contentElementsExtraction import contentElementsExtraction
from src.userempathetic.executionSteps.nodesCreation import nodesCreation
from src.userempathetic.executionSteps.sessionParsing import sessionParsing
from src.userempathetic.executionSteps.simulation import simulation
from src.userempathetic.executionSteps.lrsExtraction import lrsExtraction
from src.userempathetic.executionSteps.firstFeatureExtraction import firstFeatureExtraction
from src.userempathetic.executionSteps.userClustering import userClustering
from src.userempathetic.executionSteps.secondFeatureExtraction import secondFeatureExtraction
from src.userempathetic.executionSteps.sessionClustering import sessionClustering
from src.userempathetic.executionSteps.clusterVisualization import clusterVisualization

if __name__ == '__main__':
    print("0 = urlExtraction\n" +
          "1 = userExtraction\n" +
          "2 = contentElementsExtraction\n" +
          "3 = nodesCreation\n" +
          "4 = sessionParsing\n" +
          "5 = simulation (opcional)\n" +
          "6 = lrsExtraction\n" +
          "7 = firstFeatureExtraction\n" +
          "8 = userClustering\n" +
          "9 = secondFeatureExtraction\n" +
          "10 = sessionClustering\n" +
          "11 = clusterVisualization\n"
          )

    a = int(input("Ingrese paso de inicio:"))
    if a <= 0:
        print("URLs Extraction...")
        urlExtraction()
    if a <= 1:
        print("User Extraction...")
        userExtraction()
    if a <= 2:
        print("ContentElements Extraction...")
        contentElementsExtraction()
    if a <= 3:
        print("Nodes Creation...")
        nodesCreation()
    if a <= 4:
        print("Parsing nodes to sessions...")
        sessionParsing()
    if a <= 5:
        print("Simulating new Users, Nodes and Sessions...")
        simulation(generation = False)
    if a <= 6:
        print("LRSs Extraction...")
        lrsExtraction()
    if a <= 7:
        print("First Feature Extraction...")
        firstFeatureExtraction()
    if a <= 8:
        print("User Clustering...")
        userClustering()
    if a <= 9:
        print("Second Feature Extraction (post User Clustering)...")
        secondFeatureExtraction()
    if a <= 10:
        print("Session Clustering...")
        sessionClustering()
    if a <= 11:
        print("Clustering Visualization...")
        clusterVisualization()


