from src.userempathetic.featureExtractor.features.Feature import UserFeature
from src.userempathetic.utils.dataParsingUtils import getAllURLsIDs
from src.userempathetic.utils.sqlUtils import sqlWrapper


class UserURLsBelongingFeature(UserFeature):
    """
    Implementación de feature correspondiente al vector de pertenencia a URLs (URLs Belonging vector) para un usuario.
    Esto indica los árboles de URLs usados por el usuario, en todas sus sesiones conocidas.
    """
    tablename = 'userfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + ' (user_id,vector,feature_name) VALUES (%s,%s,%s)'

    def __init__(self, user_id, simulation=False):
        """

        Parameters
        ----------
        user_id : str | int
            id de usuario

        Returns
        -------

        """
        UserFeature.__init__(self, simulation)
        self.URLs = getAllURLsIDs()
        self.vector = [0] * len(self.URLs)
        self.user = int(user_id)

    def extract(self):
        """Implementación de extracción de feature.

        Returns
        -------

        """
        # Lectura de nodos de usuario desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select urls_id, user_id from nodes where user_id=' + str(self.user)
        userUrls = sqlCD.read(sqlRead)
        assert len(userUrls) > 0
        # Cálculo de vector de uso de URLs.
        for row in userUrls:
            l = row[0]
            for i in range(len(self.URLs)):
                if self.URLs[i] == l:
                    self.vector[i] = 1

    def extractSimulated(self):
        """Implementación de extracción de feature para usuarios simulados.

        Returns
        -------

        """
        # Lectura de nodos simulados de usuario desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select urls_id, user_id from simulatednodes where user_id=' + str(self.user)
        userUrls = sqlCD.read(sqlRead)
        assert len(userUrls) > 0

        for row in userUrls:
            l = row[0]
            for i in range(len(self.URLs)):
                if self.URLs[i] == l:
                    self.vector[i] = 1

    def __str__(self):
        return str(self.user) + ": " + str(self.vector)

    def toSQLItem(self):
        return str(self.user), ' '.join([str(x) for x in self.vector]), UserURLsBelongingFeature.__name__[:-7]
