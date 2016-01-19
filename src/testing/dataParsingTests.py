import unittest
from src.dataParsing.ExtractURLs import extractURLs
from src.dataParsing.ExtractUsers import extractUsers
from src.dataParsing.parseSessions import parseSessions
from src.utils.sqlUtils import sqlWrapper
import json
import datetime


class MyTestCase(unittest.TestCase):
    sql = sqlWrapper('PD')

    def test_extractURLs(self):
        extractURLs()
        try:
            rows = self.sql.read('SELECT * FROM urls')
            self.assertTrue(len(rows) != 0)
            for row in rows:
                id = row[0]
                urljson = row[2]
                try:
                    urls = json.loads(urljson)
                    self.assertTrue(True)
                except:
                    self.assertTrue(False)
        except:
            self.assertTrue(False)

    def test_extractUsers(self):
        extractUsers()
        try:
            rows = self.sql.read('SELECT * FROM users')
            self.assertTrue(len(rows) != 0)
            for row in rows:
                id = row[0]
                name = row[1]
                perfil = row[2]
                self.assertTrue(isinstance(id,int))
                self.assertTrue(name != '' and perfil != '')
        except:
            self.assertTrue(False)

    def test_parseSessions(self):
        parseSessions()
        try:
            rows = self.sql.read('SELECT * FROM sessions')
            self.assertTrue(len(rows) != 0)
            for row in rows:
                id = row[0]
                user = row[1]
                tinit = row[2]
                tend = row[3]
                self.assertTrue(isinstance(id,int) and isinstance(user,int))
                self.assertTrue(tinit,datetime.datetime)
                self.assertTrue(tend,datetime.datetime)
        except:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
