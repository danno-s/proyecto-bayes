"""
Paso 11
Script para ejecucion del proceso de clustering de sesiones.
"""
from src.clustering.ClusterExtractor import ClusterExtractor


def sessionClustering():
    from src.executionSteps.main import start, finish
    start()
    cE = ClusterExtractor()
    cE.extractSessionClusters()
    finish()
if __name__ == '__main__':
    sessionClustering()
