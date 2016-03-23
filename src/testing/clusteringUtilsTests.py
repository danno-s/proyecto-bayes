import unittest
from src.utils.clusteringUtils import *


class MyTestCase(unittest.TestCase):
    def test_getAllUserClusters(self):
        userClustersD = getAllUserClusters("userlrshistogramclusters")
        self.assertTrue(len(userClustersD) > 0)
        for cl_id, members in userClustersD.items():
            self.assertTrue(isinstance(cl_id, int))
            print(str(cl_id) + ": " + str(members))


if __name__ == '__main__':
    unittest.main()
