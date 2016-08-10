"""
Paso 11
Script para ejecucion del proceso de clustering de sesiones.
"""
from src.clustering.ClusterExtractor import ClusterExtractor


def sessionClustering():
    cE = ClusterExtractor()
    cE.extractSessionClusters()

if __name__ == '__main__':
    sessionClustering()
