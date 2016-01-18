import unittest
from src.dataParsing.ExtractURLs import extractURLs
from src.dataParsing.ExtractUsers import extractUsers
from src.dataParsing.parseSessions import parseSessions

class parsedDataTest(unittest.TestCase):
    def test_something(self):
        extractURLs()
        self.assertEqual(True, True)
    def test_somethingElse(self):
        extractUsers()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
