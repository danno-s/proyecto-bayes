from src.utils.sqlUtils import sqlWrapper
from src.utils.dataParsingUtils import getAllUserIDs
from src.utils.featureExtractionUtils import getAllSessionIDs

class FeatureExtractor:

        def __init__(self,userFeaturesL,sessionFeaturesL):
            """

            Parameters
            ----------
            userFeaturesL : lista de NOMBRES de clases UserFeature
            sessionFeaturesL: lista de NOMBRES de clases SessionFeature

            Returns
            -------

            """
            self.userFeaturesL = userFeaturesL
            self.sessionFeaturesL = sessionFeaturesL
            self.users = getAllUserIDs()
            self.sessionIDs = getAllSessionIDs()

        def extractUserFeatures(self):
            for userFeature in self.userFeaturesL:
                self.__extractUserFeature(userFeature)

        def extractSessionFeatures(self):
            for sessionFeature in self.sessionFeaturesL:
                self.__extractSessionFeature(sessionFeature)

        def __extractUserFeature(self,feature):
            sqlFT = sqlWrapper('FT')
            sqlFT.truncate(feature.tablename)
            print("\n"+str(feature.__name__)+":\n")
            for user in self.users:
                f = feature(user)
                f.extract()
                sqlFT.write(f.sqlWrite, f.toSQLItem())
                print(f)

        def __extractSessionFeature(self,feature):
            sqlFT = sqlWrapper('FT')
            sqlFT.truncate(feature.tablename)
            print(str(feature.__name__)+":\n")
            for sessionID in self.sessionIDs:
                f = feature(sessionID)
                f.extract()
                sqlFT.write(f.sqlWrite, f.toSQLItem())
                print(f)


if __name__ == '__main__':
    from src.featureExtraction.features.UserURLsBelongingFeature import UserURLsBelongingFeature
    from src.featureExtraction.features.UserLRSHistogramFeature import UserLRSHistogramFeature
    from src.featureExtraction.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature

    ufL = [UserURLsBelongingFeature, UserLRSHistogramFeature]
    sfL = [SessionLRSBelongingFeature]
    fE = FeatureExtractor(ufL,sfL)
    fE.extractUserFeatures()
    fE.extractSessionFeatures()
