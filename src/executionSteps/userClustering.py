"""
Paso 9
Script para ejecucion del proceso de clustering de usuarios.
"""
from src.clustering.ClusterExtractor import ClusterExtractor


def userClustering():
    cE = ClusterExtractor()
    cE.extractUserClusters()

if __name__ == '__main__':
    userClustering()
