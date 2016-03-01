#!/usr/bin/python

"""
Extrae clusters de los datos
"""

from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor

def createClusterExtractor():
    """Retorna un ClusterExtractor configurado para realizar clustering a partir de los features definidos por
     archivo de configuración del sistema.

    Returns
    -------
    ClusterExtractor
        un extractor de clusters
    """
    #TODO: PASAR A CONFIGURACION O REVISAR FEATURES EXTRAIDAS PARA DECIDIR QUE CLUSTERINGS UTILIZAR
    from src.userempathetic.clustering.clusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    from src.userempathetic.clustering.clusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
    return ClusterExtractor(userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering],sessionClusteringsL=[SessionLRSBelongingClustering, SessionUserClustersBelongingClustering])

def userclustering(cE):
    """Extrae clusters de usuarios

    Parameters
    ----------
    cE : ClusterExtractor
        un extractor de clusters con características de usuario cargadas.

    Returns
    -------

    """
    cE.extractUserClusters()

def sessionclustering(cE):
    """Extrae clusters de sesiones

    Parameters
    ----------
    cE : ClusterExtractor
        un extractor de clusters con características de sesiones cargadas.

    Returns
    -------

    """

    cE.extractSessionClusters()

if __name__ == '__main__':
    cE = createClusterExtractor()
    userclustering(cE)
    sessionclustering(cE)
    cE.visualizeClusters()
