import unittest
from src.utils.dataParsingUtils import *

from src.dataParsing.DataParser import DataParser

class MyTestCase(unittest.TestCase):

    def test_getAllUserIDs(self):
        users = DataParser().getAllUserIDs()
        self.assertTrue(len(users) > 0)
        for u_id in users:
            self.assertTrue(isinstance(u_id, int))
        self.assertEquals(users, [824, 869, 3373])

    def test_getProfileOf(self):
        profile = DataParser().getProfileOf(824)
        self.assertEquals(profile, "0109")


if __name__ == '__main__':
    unittest.main()
