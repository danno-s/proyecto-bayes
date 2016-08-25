from src.featureExtractor.features.Feature import UserFeature
from src.dataParsing.DataParser import DataParser
from src.utils.sqlUtils import sqlWrapper


class UserMacroStatesBelongingFeature(UserFeature):
    """
    Implementacion de feature correspondiente al vector de pertenencia a macro_ids (macro_ids Belonging vector) para un usuario.
    Esto indica los arboles de macro_ids usados por el usuario, en todas sus sesiones conocidas.
    """
    tablename = 'userfeatures'
    sqlWrite = 'INSERT INTO ' + tablename + \
        ' (user_id,vector,feature_name) VALUES (%s,%s,%s)'

    def __init__(self, user_id):
        """

        Parameters
        ----------
        user_id : str | int
            id de usuario

        Returns
        -------

        """
        UserFeature.__init__(self)
        self.macro_ids = DataParser().getAllMacroStateIDs()
        self.vector = [0] * len(self.macro_ids)
        self.user = int(user_id)

    def extract(self):
        """Implementacion de extraccion de feature.

        Returns
        -------

        """
        # Lectura de nodos de usuario desde 'coreData'
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select macro_id, user_id from nodes where user_id=' + \
            str(self.user)
        userMacroStates = sqlCD.read(sqlRead)
        assert len(userMacroStates) > 0
        # Calculo de vector de uso de macro_ids.
        for row in userMacroStates:
            l = row[0]
            for i in range(len(self.macro_ids)):
                if self.macro_ids[i] == l:
                    self.vector[i] = 1

    def __str__(self):
        return str(self.user) + ": " + str(self.vector)

    def toSQLItem(self):
        return str(self.user), ' '.join([str(x) for x in self.vector]), self.__class__.__name__[:-7]
