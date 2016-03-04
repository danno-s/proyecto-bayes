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
from src.userempathetic.utils.sqlUtils import sqlWrapper

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
    sqlFT = sqlWrapper('FT')
    sqlFT.truncate('userfeatures')
    sqlFT.truncate('sessionfeatures')
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
    session_features = Config().getArray("session_features")
    if "SessionUserClustersBelonging" in session_features:
        sfL.append(SessionUserClustersBelongingFeature)

    fE = FeatureExtractor(sessionFeaturesL=sfL, simulation=simulation)
    fE.extractSessionFeatures()


if __name__ == '__main__':
    extractFeatures()
    extractPostClusteringFeatures()
