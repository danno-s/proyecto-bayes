"""
Paso 12
Script para ejecucion de la visualizacion de clusters extraidos.
"""
from src.view.ClusterView import ClusterView


def clusterVisualization():
    cv = ClusterView()
    cv.view()

if __name__ == '__main__':
    clusterVisualization()
