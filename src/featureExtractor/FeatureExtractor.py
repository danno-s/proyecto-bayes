"""
Elemento encargado de extraer features (caracteristicas) de usuarios y sesiones capturadas.
"""
from src.utils.sqlUtils import sqlWrapper
from src.utils.featureExtractionUtils import getAllSessionIDs
from src.dataParsing.DataParser import DataParser


class FeatureExtractor:
    """
    Clase encargada de extraer features de usuarios y sesiones.
    """

    def __init__(self, userFeaturesL=None, sessionFeaturesL=None):
        """Constructor

            Parameters
            ----------
            userFeaturesL : [class]
                lista de clases UserFeature
            sessionFeaturesL : [class]
                lista de clases SessionFeature

            Returns
            -------

            """
        self.userFeaturesL = userFeaturesL or []
        self.sessionFeaturesL = sessionFeaturesL or []
        self.users = DataParser().getAllUserIDs()
        self.sessionIDs = getAllSessionIDs()

    def extractUserFeatures(self):
        """Recorre todas las features de usuarios y realiza la extraccion de feature para cada una.

        Returns
        -------

        """
        for userFeature in self.userFeaturesL:
            self.__extractUserFeature(userFeature)

    def extractSessionFeatures(self):
        """Recorre todas las features de sesiones y realiza la extraccion de feature para cada una.

        Returns
        -------

        """
        for sessionFeature in self.sessionFeaturesL:
            self.__extractSessionFeature(sessionFeature)

    def __extractUserFeature(self, feature):
        """ Extrae el feature de cada usuario y lo agrega a la tabla correspondiente en la DB 'features'

        Parameters
        ----------
        feature : UserFeature
            clase implementacion de UserFeature.
        Returns
        -------

        """
        sqlFT = sqlWrapper('FT')
        print("\n" + str(feature.__name__) + ":\n")
        for user in self.users:
            f = feature(user)
            try:
                f.extract()
            except AssertionError:
                continue
            sqlFT.write(f.sqlWrite, f.toSQLItem())
            if '[]' not in str(f):
                print(f)

    def __extractSessionFeature(self, feature):
        """ Extrae el feature de cada sesion y lo agrega a la tabla correspondiente en la DB 'features'

        Parameters
        ----------
        feature : SessionFeature
            clase implementacion de SessionFeature.
        Returns
        -------

        """
        sqlFT = sqlWrapper('FT')
        print("\n" + str(feature.__name__) + ":\n")
        for sessionID in self.sessionIDs:
            f = feature(sessionID)
            f.extract()
            sqlFT.write(f.sqlWrite, f.toSQLItem())
            if '[]' not in str(f):
                print(f)
