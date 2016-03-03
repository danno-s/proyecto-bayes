import unittest
from src.userempathetic.utils.dataParsingUtils import *


class MyTestCase(unittest.TestCase):
    def test_getAllUserIDs(self):
        users = getAllUserIDs()
        self.assertTrue(len(users) > 0)
        for u_id in users:
            self.assertTrue(isinstance(u_id, int))
        self.assertEquals(users, [824, 869, 3373])

    def test_getProfileOf(self):
        profile = getProfileOf(824)
        self.assertEquals(profile, "0109")


if __name__ == '__main__':
    unittest.main()
