import unittest
from src.userempathetic.utils.clusteringUtils import *


class MyTestCase(unittest.TestCase):
    def test_getAllUserClusters(self):
        userClustersD = getAllUserClusters("userlrshistogramclusters")
        self.assertTrue(len(userClustersD) > 0)
        for id, members in userClustersD.items():
            self.assertTrue(isinstance(id, int))
            print(str(id) + ": " + str(members))


if __name__ == '__main__':
    unittest.main()
