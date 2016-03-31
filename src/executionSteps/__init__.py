"""
Este modulo ordena los distintos scripts que componen los pasos del sistema, de manera de permitir
una ejecucion de un unico paso o de realizar una ejecucion secuencial a partir de un cierto paso.

El orden de los pasos de ejecucion es el siguiente:

    1. urlExtraction
    2. userExtraction
    3. contentElementsExtraction
    4. nodesCreation
    5. sessionParsing
    6. simulation (opcional)
    7. lrsExtraction
    8. firstFeatureExtraction
    9. userClustering
    10. secondFeatureExtraction
    11. sessionClustering
    12. clusterVisualization

"""