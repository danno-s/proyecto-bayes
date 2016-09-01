"""
Ejecuta todos los pasos del sistema a partir del paso indicado en consola.
"""
from src.executionSteps.macroStatesExtraction import macroStatesExtraction
from src.executionSteps.urlExtraction import urlExtraction
from src.executionSteps.userExtraction import userExtraction
from src.executionSteps.contentElementsExtraction import contentElementsExtraction
from src.executionSteps.nodesCreation import nodesCreation
from src.executionSteps.sessionParsing import sessionParsing
from src.executionSteps.simulation import simulation
from src.executionSteps.lrsExtraction import lrsExtraction
from src.executionSteps.firstFeatureExtraction import firstFeatureExtraction
from src.executionSteps.userClustering import userClustering
from src.executionSteps.secondFeatureExtraction import secondFeatureExtraction
from src.executionSteps.sessionClustering import sessionClustering
from src.executionSteps.clusterVisualization import clusterVisualization
simulate = False

if __name__ == '__main__':

    print("0 = macroStateExtraction\n" +
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
    b = input("Ingrese paso de fin:")
    if b == '': b = 11
    else: b = int(b)

    if a <= 0:
        print("MacroStates Extraction...")
        #urlExtraction()
        macroStatesExtraction()
        if b== 0: exit()

    if a <= 1:
        print("User Extraction...")
        userExtraction()
        if b == 1: exit()
    if a <= 2:
        print("ContentElements Extraction...")
        contentElementsExtraction()
        if b == 2: exit()
    if a <= 3:
        print("Nodes Creation...")
        nodesCreation()
        if b == 3: exit()
    if a <= 4:
        print("Parsing nodes to sessions...")
        sessionParsing()
        if b == 4: exit()
    if a <= 5 and simulate == True:
        print("Simulating new Users, Nodes and Sessions...")
        simulation(generation=False)
        if b == 5: exit()
    if a <= 6:
        print("LRSs Extraction...")
        lrsExtraction()
        if b == 6: exit()
    if a <= 7:
        print("First Feature Extraction...")
        firstFeatureExtraction()
        if b == 7: exit()
    if a <= 8:
        print("User Clustering...")
        userClustering()
        if b == 8: exit()
    if a <= 9:
        print("Second Feature Extraction (post User Clustering)...")
        secondFeatureExtraction()
        if b == 9: exit()
    if a <= 10:
        print("Session Clustering...")
        sessionClustering()
        if b == 10: exit()
    if a <= 11:
        print("Clustering Visualization...")
        clusterVisualization()
        if b== 11: exit()


def start():
    """
    Permite deshabilitar verificacion de llaves secundarias para vaciar tablas de un paso en particular.
    Returns
    -------

    """
    from src.utils.sqlUtils import sqlWrapper
    try:
        sqlPD = sqlWrapper('PD')
        sqlPD.setGlobalFKChecks('0')
    except:
        print("ERROR")


def finish():
    """
    Permite habilitar verificacion de llaves secundarias una vez ejecutado un paso.
    Returns
    -------

    """
    from src.utils.sqlUtils import sqlWrapper
    try:
        sqlPD = sqlWrapper('PD')
        sqlPD.setGlobalFKChecks('1')
    except:
        print("ERROR")
