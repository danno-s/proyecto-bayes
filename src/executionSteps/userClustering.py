"""
Paso 9
Script para ejecucion del proceso de clustering de usuarios.
"""
from src.clustering.ClusterExtractor import ClusterExtractor


def userClustering():
    from src.executionSteps.main import start, finish
    start()
    cE = ClusterExtractor()
    cE.extractUserClusters()
    finish()
if __name__ == '__main__':
    userClustering()
