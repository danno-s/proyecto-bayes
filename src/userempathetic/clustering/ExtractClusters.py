#!/usr/bin/python

"""
Extrae clusters de los datos
"""

from src.userempathetic.clustering.ClusterExtractor import ClusterExtractor
from src.userempathetic.utils.loadConfig import Config
from src.userempathetic.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
from src.userempathetic.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import \
        SessionUserClustersBelongingClustering
from src.userempathetic.clustering.clusterings.sessionclusterings.CompositeSessionClustering import CompositeSessionClustering
from src.userempathetic.clustering.clusterings.sessionclusterings.DirectSessionClustering import DirectSessionClustering
from src.userempathetic.clustering.clusterings.sessionclusterings.FullSessionClustering import FullSessionClustering
from src.userempathetic.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
from src.userempathetic.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
from src.userempathetic.clustering.clusterings.userclusterings.FullUserClustering import FullUserClustering

userClusteringsD = {
    "UserLRSHistogram": UserLRSHistogramClustering,
    "UserURLsBelonging": UserURLsBelongingClustering,
    "FullUser": FullUserClustering
    }

sessionClusteringsD = {
    "SessionLRSBelonging": SessionLRSBelongingClustering,
    "SessionUserClustersBelonging": SessionUserClustersBelongingClustering,
    "FullSession": FullSessionClustering,
    "DirectSession": DirectSessionClustering,
    "CompositeSession": CompositeSessionClustering
    }

def createClusterExtractor():
    """Retorna un ClusterExtractor configurado para realizar clustering a partir de los features definidos por
     archivo de configuración del sistema.

    Returns
    -------
    ClusterExtractor
        un extractor de clusters
    """

    ucL = list()
    scL = list()
    scConfD = dict()
    ucConfD = dict()
    user_clusteringD = Config.getDict("user_clustering")
    session_clusteringD = Config.getDict("session_clustering")
    for k,v in session_clusteringD.items():
        if k in sessionClusteringsD.keys():
            scConfD[sessionClusteringsD[k]]=v

    for k,v in user_clusteringD.items():
        if k in userClusteringsD.keys():
            ucConfD[userClusteringsD[k]]=v

    return ClusterExtractor(userClusteringsConfD = ucConfD,sessionClusteringsConfD = scConfD)


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
