"""
Elemento encargado de extraer features (características) de usuarios y sesiones capturadas.
"""
from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.utils.dataParsingUtils import getAllUserIDs
from src.userempathetic.utils.featureExtractionUtils import getAllSessionIDs, getAllSimulSessionIDs


class FeatureExtractor:
    """
    Clase encargada de extraer features de usuarios y sesiones.
    """
    def __init__(self, userFeaturesL=None, sessionFeaturesL=None,simulation=False):
        """Constructor

            Parameters
            ----------
            userFeaturesL : [class]
                lista de clases UserFeature
            sessionFeaturesL : [class]
                lista de clases SessionFeature
            simulation : bool
                Modo de ejecución del extractor. Si es True, utiliza las tablas con elementos simulados.

            Notes
                En el caso de simulación, se debe haber realiado correctamente la simulación de nodos, usuarios
                y sesiones para que el FeatureExtractor funcione.
            Returns
            -------

            """
        self.userFeaturesL = userFeaturesL or []
        self.sessionFeaturesL = sessionFeaturesL or []
        self.users = getAllUserIDs()
        if simulation:
            self.simulation = simulation
        if not simulation:
            self.simulation = False
            self.sessionIDs = getAllSessionIDs()
        else:
            self.sessionIDs = getAllSimulSessionIDs()

    def extractUserFeatures(self):
        """Recorre todas las features de usuarios y realiza la extracción de feature para cada una.

        Returns
        -------

        """
        for userFeature in self.userFeaturesL:
            self.__extractUserFeature(userFeature)

    def extractSessionFeatures(self):
        """Recorre todas las features de sesiones y realiza la extracción de feature para cada una.

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
            clase implementación de UserFeature.
        Returns
        -------

        """
        sqlFT = sqlWrapper('FT')
        sqlFT.truncate(feature.tablename)
        print("\n" + str(feature.__name__) + ":\n")
        for user in self.users:
            f = feature(user)
            if not self.simulation:
                f.extract()
            else:
                f.extractSimulated()
            sqlFT.write(f.sqlWrite, f.toSQLItem())
            if len(f.vector) >0:
                print(f)

    def __extractSessionFeature(self, feature):
        """ Extrae el feature de cada sesión y lo agrega a la tabla correspondiente en la DB 'features'

        Parameters
        ----------
        feature : SessionFeature
            clase implementación de SessionFeature.
        Returns
        -------

        """
        sqlFT = sqlWrapper('FT')
        sqlFT.truncate(feature.tablename)
        print("\n" + str(feature.__name__) + ":\n")
        for sessionID in self.sessionIDs:
            f = feature(sessionID)
            if not self.simulation:
                f.extract()
            else:
                f.extractSimulated()
            sqlFT.write(f.sqlWrite, f.toSQLItem())
            if len(f.vector) >0:
                print(f)
