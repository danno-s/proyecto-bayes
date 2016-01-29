from src.featureExtraction.features.Feature import UserFeature
from src.utils.sqlUtils import sqlWrapper
from src.utils.dataParsingUtils import getAllURLsIDs

class UserURLsBelongingFeature(UserFeature):
    URLs = getAllURLsIDs()
    tablename = 'userurlsbelongingfeatures'
    sqlWrite = 'INSERT INTO '+tablename+ ' (user_id,vector) VALUES (%s,%s)'

    def __init__(self,user):
        UserFeature.__init__(self)
        self.vector = [0] * len(self.URLs)
        self.user = int(user)
        pass

    def extract(self):
        sqlCD = sqlWrapper(db='CD')
        sqlRead = 'select urls_id, user_id from nodes where user_id='+str(self.user)
        userUrls = sqlCD.read(sqlRead)
        assert len(userUrls) > 0

        for row in userUrls:
            l = row[0]
            for i in range(len(self.URLs)):
                if self.URLs[i] == l:
                    self.vector[i] = 1

    def __str__(self):
        return str(self.user)+": "+ str(self.vector)

    def toSQLItem(self):
        return str(self.user), ' '.join([str(x) for x in self.vector])
