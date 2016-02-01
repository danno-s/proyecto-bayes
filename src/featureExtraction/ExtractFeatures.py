from src.featureExtractor.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature
from src.featureExtractor.features.UserLRSHistogramFeature import UserLRSHistogramFeature
from src.featureExtractor.features.UserURLsBelongingFeature import UserURLsBelongingFeature

from src.featureExtractor.FeatureExtractor import FeatureExtractor
from src.utils.loadConfig import Config


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

    fE = FeatureExtractor(ufL,sfL)
    fE.extractUserFeatures()
    fE.extractSessionFeatures()

if __name__ == '__main__':
    extractFeatures()

