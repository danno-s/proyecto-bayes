import unittest

from src.featureExtraction.calcLRSs import calcLRSs
from src.featureExtraction.calcUserLRSHistograms import calcUserLRSHistograms
from src.featureExtraction.extractUserClusteringFeatures import extractUserClusteringFeatures
from src.featureExtraction.linkSessionsWithLRSs import linkSessionsWithLRSs
from src.utils.featureExtractionUtils import *
from src.utils.sqlUtils import sqlWrapper


class MyTestCase(unittest.TestCase):
    sql = sqlWrapper('PD')

    def test_calcLRSs(self):
        try:
            calcLRSs()
            rows = self.sql.read('SELECT * FROM lrss')
            self.assertTrue(len(rows) != 0)
            for row in rows:
                id = row[0]
                seq = row[1]
                count = row[2]
                self.assertTrue(isinstance(id,int))
                self.assertTrue(isinstance(seq,str))
                self.assertTrue(isinstance(count,int))
                L=seq.split(' ')
                self.assertTrue(len(L)>0)
        except:
            self.assertTrue(False)
    '''
    def test_extractUserClusteringFeatures(self):
        extractUserClusteringFeatures()
        try:
            rows = self.sql.read('SELECT * FROM userclusteringfeatures')
            self.assertTrue(len(rows) != 0)
            for row in rows:
                id = row[0]
                featurevector = row[1].split(' ')
                self.assertTrue(isinstance(id,int))
                self.assertTrue(len(featurevector)>0)
                for x in featurevector:
                    self.assertTrue(x == '1' or x == '0')
        except:
            self.assertTrue(False)
    '''
    def test_linkSessionWithLRSs(self):
        linkSessionsWithLRSs()
        try:
            rows = self.sql.read('SELECT * FROM sessionlrssfeatures')
            self.assertTrue(len(rows) != 0)
            for row in rows:
                id = row[0]
                featurevector = row[1].split(' ')
                self.assertTrue(isinstance(id,int))
                self.assertTrue(len(featurevector)>0)
                for x in featurevector:
                    self.assertTrue(x == '1' or x == '0')
        except:
            self.assertTrue(False)

    def test_calcUserLRSHistograms(self):
        calcUserLRSHistograms()
    #    try:
        rows = self.sql.read('SELECT * FROM userlrshistograms')
        self.assertTrue(len(rows) != 0)
        try:
            for row in rows:
                id = row[0]
                hist = row[1].split(' ')
                self.assertTrue(isinstance(id,int))
                self.assertTrue(len(hist)>0)
                hist_f = [float(x) for x in hist]
                for x in hist_f:
                    self.assertTrue(x >= 0.0 and x <= 1.0)
                s = sum(hist_f)
                if s != 0.0:
                    self.assertAlmostEquals(s,1.0,0.1)
        except:
            self.assertTrue(False)

    def test_consecutiveIdxs(self):
        s = [0,1,2,3,4]
        gen = consecutiveIdxs(s,5)
        x = gen.__next__()
        self.assertEquals(list(x),s)
        gen = consecutiveIdxs(s,4)
        x = gen.__next__()
        self.assertEquals(x,(0,1,2,3))
        x = gen.__next__()
        self.assertEquals(x,(1,2,3,4))
        try:
            x = gen.__next__()
            self.assertTrue(False)
        except StopIteration:
            self.assertTrue(True)
        gen = consecutiveIdxs(s,3)
        x = gen.__next__()
        self.assertEquals(x,(0,1,2))
        x = gen.__next__()
        self.assertEquals(x,(1,2,3))
        x = gen.__next__()
        self.assertEquals(x,(2,3,4))
        gen = consecutiveIdxs(s,1)
        try:
            x = gen.__next__()
        except StopIteration:
            self.assertTrue(True)
        gen = consecutiveIdxs(s,2)
        try:
            x = gen.__next__()
            self.assertEqual(x,(0,1))
            x = gen.__next__()
            self.assertEqual(x,(1,2))
            x = gen.__next__()
            self.assertEqual(x,(2,3))
            x = gen.__next__()
            self.assertEqual(x,(3,4))
            x = gen.__next__()
            self.assertTrue(False)
        except StopIteration:
            self.assertTrue(True)

    def test_contains(self):
        a = '0 1 2 3'
        b = '0 1 2 3 4'
        self.assertTrue(contains(a,b))
        self.assertFalse(contains(b,a))
        a = '0 1 2 3 4'
        self.assertFalse(contains(a,b))

    def test_isSubContained(self):
        a = ['0 1 2 3 4','3 4 5 6 7','0 1 2','9 9']
        b = '3 4'
        self.assertTrue(isSubContained(b,a))
        b = '9 9'
        self.assertFalse(isSubContained(b,a))
        b = '1 2 3 4 5 6 7'
        self.assertFalse(isSubContained(b,a))

    def test_subsequences(self):
        gen = subsequences(['A','B','C'])
        x = gen.__next__()
        self.assertEquals(x,'A B')
        x = gen.__next__()
        self.assertEquals(x,'B C')
        x = gen.__next__()
        self.assertEquals(x,'A B C')
        try:
            x = gen.__next__()
            self.assertTrue(False)
        except StopIteration:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
