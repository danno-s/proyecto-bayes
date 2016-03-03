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
    # TODO: PASAR A CONFIGURACION O REVISAR FEATURES EXTRAIDAS PARA DECIDIR QUE CLUSTERINGS UTILIZAR
    from src.userempathetic.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
    from src.userempathetic.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
    from src.userempathetic.clustering.clusterings.sessionclusterings.FullSessionClustering import FullSessionClustering
    from src.userempathetic.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    from src.userempathetic.clustering.clusterings.userclusterings.FullUserClustering import FullUserClustering

    return ClusterExtractor(sessionClusteringsL=[SessionLRSBelongingClustering, SessionUserClustersBelongingClustering,FullSessionClustering],
                          userClusteringsL=[UserLRSHistogramClustering, UserURLsBelongingClustering, FullUserClustering])


def userclustering(clusterExtractor):
    """Extrae clusters de usuarios

    Parameters
    ----------
    clusterExtractor : ClusterExtractor
        un extractor de clusters con características de usuario cargadas.

    Returns
    -------

    """
    clusterExtractor.extractUserClusters()


def sessionclustering(clusterExtractor):
    """Extrae clusters de sesiones

    Parameters
    ----------
    clusterExtractor : ClusterExtractor
        un extractor de clusters con características de sesiones cargadas.

    Returns
    -------

    """

    clusterExtractor.extractSessionClusters()


if __name__ == '__main__':
    cE = createClusterExtractor()
    userclustering(cE)
    sessionclustering(cE)
    cE.visualizeClusters()
