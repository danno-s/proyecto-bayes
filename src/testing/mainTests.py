import unittest
from src.main import *


class MyTestCase(unittest.TestCase):

    def test_dataParsing(self):
        parseData()
        self.assertTrue(True)

    def test_featureExtraction(self):
        extractFeatures()
        self.assertTrue(True)

    def test_clustering(self):
        clustering()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
