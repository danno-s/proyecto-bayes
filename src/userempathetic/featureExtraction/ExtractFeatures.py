#!/usr/bin/python

"""
Extrae vectores descriptores de los datos
"""

from src.userempathetic.featureExtractor.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature
from src.userempathetic.featureExtractor.features.SessionUserClustersBelongingFeature import SessionUserClustersBelongingFeature
from src.userempathetic.featureExtractor.features.UserLRSHistogramFeature import UserLRSHistogramFeature
from src.userempathetic.featureExtractor.features.UserURLsBelongingFeature import UserURLsBelongingFeature
from src.userempathetic.featureExtractor.FeatureExtractor import FeatureExtractor
from src.userempathetic.utils.loadConfig import Config


def extractFeatures():
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
    if "SessionUserClustersBelonging" in session_features:
        sfL.append(SessionUserClustersBelongingFeature)

    fE = FeatureExtractor(ufL,sfL)
    fE.extractUserFeatures()
    fE.extractSessionFeatures()

if __name__ == '__main__':
    extractFeatures()

