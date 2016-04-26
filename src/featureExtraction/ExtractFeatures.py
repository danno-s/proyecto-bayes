#!/usr/bin/python

"""
Extrae vectores descriptores (features) de los datos
"""

from src.featureExtractor.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature
from src.featureExtractor.features.SessionUserClustersBelongingFeature import \
    SessionUserClustersBelongingFeature
from src.featureExtractor.features.SessionDistanceFeature import SessionDistanceFeature

from src.featureExtractor.features.UserLRSHistogramFeature import UserLRSHistogramFeature
from src.featureExtractor.features.UserURLsBelongingFeature import UserURLsBelongingFeature

from src.featureExtractor.FeatureExtractor import FeatureExtractor
from src.utils.loadConfig import Config

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


def extractFeatures():
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
    fE = FeatureExtractor(ufL, sfL)
    fE.extractUserFeatures()
    fE.extractSessionFeatures()


def extractPostClusteringFeatures():
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

    fE = FeatureExtractor(sessionFeaturesL=sfL)
    fE.extractSessionFeatures()


if __name__ == '__main__':
    extractFeatures()
    extractPostClusteringFeatures()