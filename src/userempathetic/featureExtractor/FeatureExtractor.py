from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.utils.dataParsingUtils import getAllUserIDs
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs


class FeatureExtractor:
    def __init__(self, userFeaturesL=None, sessionFeaturesL=None):
        """

            Parameters
            ----------
            userFeaturesL : lista de NOMBRES de clases UserFeature
            sessionFeaturesL: lista de NOMBRES de clases SessionFeature

            Returns
            -------

            """
        self.userFeaturesL = userFeaturesL or []
        self.sessionFeaturesL = sessionFeaturesL or []
        self.users = getAllUserIDs()
        self.sessionIDs = getAllSessionIDs()

    def extractUserFeatures(self):
        for userFeature in self.userFeaturesL:
            self.__extractUserFeature(userFeature)

    def extractSessionFeatures(self):
        for sessionFeature in self.sessionFeaturesL:
            self.__extractSessionFeature(sessionFeature)

    def __extractUserFeature(self, feature):
        sqlFT = sqlWrapper('FT')
        sqlFT.truncate(feature.tablename)
        print("\n" + str(feature.__name__) + ":\n")
        for user in self.users:
            f = feature(user)
            f.extract()
            sqlFT.write(f.sqlWrite, f.toSQLItem())
            print(f)

    def __extractSessionFeature(self, feature):
        sqlFT = sqlWrapper('FT')
        sqlFT.truncate(feature.tablename)
        print("\n" + str(feature.__name__) + ":\n")
        for sessionID in self.sessionIDs:
            f = feature(sessionID)
            f.extract()
            sqlFT.write(f.sqlWrite, f.toSQLItem())
            print(f)
