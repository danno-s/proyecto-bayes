from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.utils.loadConfig import Config

sessionFeaturesL = Config().getArray("session_features")


def getFeatureOfSession(session_id, feature):
    assert feature in sessionFeaturesL
    sqlFT = sqlWrapper('FT')
    sqlRead = "SELECT vector FROM " + feature.lower() + "features WHERE session_id =" + str(session_id)
    row = sqlFT.read(sqlRead)
    return [int(x) for x in row[0][0].split(' ')]
