#!/usr/bin/python

"""
Extrae vectores descriptores (features) de los datos
"""

from src.userempathetic.featureExtractor.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature
from src.userempathetic.featureExtractor.features.SessionUserClustersBelongingFeature import \
    SessionUserClustersBelongingFeature
from src.userempathetic.featureExtractor.features.UserLRSHistogramFeature import UserLRSHistogramFeature
from src.userempathetic.featureExtractor.features.UserURLsBelongingFeature import UserURLsBelongingFeature
from src.userempathetic.featureExtractor.FeatureExtractor import FeatureExtractor
from src.userempathetic.utils.loadConfig import Config


def extractFeatures():
    """ Extrae todos los features de usuario y sesiones ingresados en el archivo de configuración del sistema y que no
    requieren de haber realizado clustering previamente.

    Returns
    -------

    """
    ufL = list()
    user_features = Config().getArray("user_features")
    if "UserURLsBelonging" in user_features:
        ufL.append(UserURLsBelongingFeature)
    if "UserLRSHistogram" in user_features:
        ufL.append(UserLRSHistogramFeature)

    sfL = list()
    session_features = Config().getArray("session_features")
    if "SessionLRSBelonging" in session_features:
        sfL.append(SessionLRSBelongingFeature)

    fE = FeatureExtractor(ufL, sfL)
    fE.extractUserFeatures()
    fE.extractSessionFeatures()


def extractPostClusteringFeatures():
    """ Extrae todos los features de usuario y sesiones ingresados en el archivo de configuración del sistema
    que requieren haber realizado clustering previamente.

    Returns
    -------

    """
    sfL = list()
    session_features = Config().getArray("session_features")
    if "SessionUserClustersBelonging" in session_features:
        sfL.append(SessionUserClustersBelongingFeature)

    fE = FeatureExtractor(sessionFeaturesL=sfL)
    fE.extractSessionFeatures()


if __name__ == '__main__':
    extractFeatures()
    extractPostClusteringFeatures()
