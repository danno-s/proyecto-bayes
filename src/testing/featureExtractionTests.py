import unittest

from src.featureExtraction.calcLRSs import calcLRSs
from src.utils.featureExtractionUtils import *
from src.utils.sqlUtils import sqlWrapper
from src.featureExtractor.FeatureExtractor import FeatureExtractor
from src.featureExtractor.features.UserLRSHistogramFeature import UserLRSHistogramFeature
from src.featureExtractor.features.UserMacroStatesBelongingFeature import UserMacroStatesBelongingFeature
from src.featureExtractor.features.SessionLRSBelongingFeature import SessionLRSBelongingFeature


class MyTestCase(unittest.TestCase):
    sqlCD = sqlWrapper('CD')
    sqlFT = sqlWrapper('FT')

    def test_calcLRSs(self):
        calcLRSs()
        rows = self.sqlCD.read('SELECT * FROM lrss')
        self.assertTrue(len(rows) != 0)
        for row in rows:
            lrs_id = row[0]
            seq = row[1]
            count = row[2]
            self.assertTrue(isinstance(lrs_id, int))
            self.assertTrue(isinstance(seq, str))
            self.assertTrue(isinstance(count, int))
            L = seq.split(' ')
            self.assertTrue(len(L) > 0)

    def test_consecutiveIdxs(self):
        s = [0, 1, 2, 3, 4]
        gen = consecutiveIdxs(s, 5)
        x = gen.__next__()
        self.assertEquals(list(x), s)
        gen = consecutiveIdxs(s, 4)
        x = gen.__next__()
        self.assertEquals(x, (0, 1, 2, 3))
        x = gen.__next__()
        self.assertEquals(x, (1, 2, 3, 4))
        try:
            x = gen.__next__()
            self.assertTrue(False)
        except StopIteration:
            self.assertTrue(True)
        gen = consecutiveIdxs(s, 3)
        x = gen.__next__()
        self.assertEquals(x, (0, 1, 2))
        x = gen.__next__()
        self.assertEquals(x, (1, 2, 3))
        x = gen.__next__()
        self.assertEquals(x, (2, 3, 4))
        gen = consecutiveIdxs(s, 1)
        try:
            x = gen.__next__()
        except StopIteration:
            self.assertTrue(True)
        gen = consecutiveIdxs(s, 2)
        try:
            x = gen.__next__()
            self.assertEqual(x, (0, 1))
            x = gen.__next__()
            self.assertEqual(x, (1, 2))
            x = gen.__next__()
            self.assertEqual(x, (2, 3))
            x = gen.__next__()
            self.assertEqual(x, (3, 4))
            x = gen.__next__()
            self.assertTrue(False)
        except StopIteration:
            self.assertTrue(True)

    def test_contains(self):
        a = '0 1 2 3'
        b = '0 1 2 3 4'
        self.assertTrue(contains(a, b))
        self.assertFalse(contains(b, a))
        a = '0 1 2 3 4'
        self.assertFalse(contains(a, b))

    def test_isSubContained(self):
        a = ['0 1 2 3 4', '3 4 5 6 7', '0 1 2', '9 9']
        b = '3 4'
        self.assertTrue(isSubContained(b, a))
        b = '9 9'
        self.assertFalse(isSubContained(b, a))
        b = '1 2 3 4 5 6 7'
        self.assertFalse(isSubContained(b, a))

    def test_subsequences(self):
        gen = subsequences(['A', 'B', 'C'])
        x = gen.__next__()
        self.assertEquals(x, 'A B')
        x = gen.__next__()
        self.assertEquals(x, 'B C')
        x = gen.__next__()
        self.assertEquals(x, 'A B C')
        try:
            x = gen.__next__()
            self.assertTrue(False)
        except StopIteration:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
