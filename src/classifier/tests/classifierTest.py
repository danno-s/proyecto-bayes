from src.classifier.userClassifier import UserClassifier
from src.clustering.clusterings.userclusterings.\
    UserMacroStatesBelongingClustering import UserMacroStatesBelongingClustering
from src.utils.clusteringUtils import getPerformedUserClusterings
import unittest

class TestUserClassifier(unittest.TestCase):
    cl = getPerformedUserClusterings()[0]
    uc = UserClassifier(cl)
    def test_predict(self):
        vec = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,\
               1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        pr = self.uc.predict(vec)
        self.assertEquals(pr, 2)

if __name__ == "__main__":
    unittest.main()
