"""
Paso 12
Script para ejecución de la visualización de clusters extraídos.
"""
from src.view.ClusterView import ClusterView


def clusterVisualization():
    cv = ClusterView()
    cv.view()

if __name__ == '__main__':
    clusterVisualization()

