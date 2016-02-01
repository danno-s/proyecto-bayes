import unittest
from src.userempathetic.main import *


class MyTestCase(unittest.TestCase):

    def test_dataParsing(self):
        try:
            parseData()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_featureExtraction(self):
        try:
            extractFeatures()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_clustering(self):
        try:
            clustering()
            self.assertTrue(True)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
