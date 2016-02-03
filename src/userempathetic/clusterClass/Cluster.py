class Cluster:

    def __init__(self, elements, label, clusteringType=None):
        self.label = label
        self.elements = [x[0] for x in elements]
        self.ids = [x[1] for x in elements]
        self.n_elements = len(self.elements)
        assert self.n_elements > 0
        self.features_dim = len(self.elements[0])
        self.clusteringType = clusteringType or ""

    def getCentroid(self):
        return [sum([value[x]/self.n_elements for value in self.elements]) for x in range(self.features_dim)]

    def getMax(self):
        return [max([value[x] for value in self.elements]) for x in range(self.features_dim)]

    def getMin(self):
        return [min([value[x] for value in self.elements]) for x in range(self.features_dim)]


    def __str__(self):
        return "Cluster "+ str(self.label)+",\t#"+str(self.n_elements)+" inliers"\
                                                                    "\n Elements IDs:\n"+ str(self.ids)+\
                                                                    "\n Elements Features:\n"+ str(self.elements)