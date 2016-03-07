#!/usr/bin/python

"""
Extrae vectores descriptores (features) de los datos
"""

from src.userempathetic.featureExtractor.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature
from src.userempathetic.featureExtractor.features.SessionUserClustersBelongingFeature import \
    SessionUserClustersBelongingFeature
from src.userempathetic.featureExtractor.features.SessionDistanceFeature import SessionDistanceFeature

from src.userempathetic.featureExtractor.features.UserLRSHistogramFeature import UserLRSHistogramFeature
from src.userempathetic.featureExtractor.features.UserURLsBelongingFeature import UserURLsBelongingFeature

from src.userempathetic.featureExtractor.FeatureExtractor import FeatureExtractor
from src.userempathetic.utils.loadConfig import Config
from src.userempathetic.utils.sqlUtils import sqlWrapper

userFeaturesD = {
    "UserURLsBelonging": UserURLsBelongingFeature,
    "UserLRSHistogram": UserLRSHistogramFeature
    }
sessionFeaturesD = {
    "SessionLRSBelonging": SessionLRSBelongingFeature,
    "SessionDistance": SessionDistanceFeature
    }
sessionPostClusteringFeaturesD = {
    "SessionUserClustersBelonging": SessionUserClustersBelongingFeature
    }


def extractFeatures(simulation=False):
    """ Extrae todos los features de usuario y sesiones ingresados en el archivo de configuración del sistema y que no
    requieren de haber realizado clustering previamente.

    Parameters
    ----------
    simulation : bool
        Modo de ejecución.

    Returns
    -------

    """
    ufL = list()
    user_features = Config.getArray("user_features")
    for uf in user_features:
        if uf in userFeaturesD.keys():
            ufL.append(userFeaturesD[uf])

    sfL = list()
    session_features = Config.getArray("session_features")
    for sf in session_features:
        if sf in sessionFeaturesD.keys():
            print(sf)
            sfL.append(sessionFeaturesD[sf])
    fE = FeatureExtractor(ufL, sfL, simulation=simulation)
    fE.extractUserFeatures()
    fE.extractSessionFeatures()


def extractPostClusteringFeatures(simulation=False):
    """ Extrae todos los features de usuario y sesiones ingresados en el archivo de configuración del sistema
    que requieren haber realizado clustering previamente.

    Parameters
    ----------
    simulation : bool
        Modo de ejecución.

    Returns
    -------

    """
    sfL = list()
    session_features = Config.getArray("session_features")
    for sf in session_features:
        if sf in sessionPostClusteringFeaturesD.keys():
            sfL.append(sessionPostClusteringFeaturesD[sf])

    fE = FeatureExtractor(sessionFeaturesL=sfL, simulation=simulation)
    fE.extractSessionFeatures()


if __name__ == '__main__':
    extractFeatures()
    extractPostClusteringFeatures()
