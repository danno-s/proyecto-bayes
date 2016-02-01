import unittest
from src.simulated.utils.sqlUtils import sqlWrapper


class MyTestCase(unittest.TestCase):

    def test_loadConnection(self):
        try:
            s = sqlWrapper('PD')
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_loadConnectionFailure(self):
        try:
            s = sqlWrapper('XD')
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_readSQL(self):
        s = sqlWrapper('PD')
        self.assertTrue(True)
        try:
            row = s.read('SELECT * from users')
            self.assertTrue(True)
        except:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
