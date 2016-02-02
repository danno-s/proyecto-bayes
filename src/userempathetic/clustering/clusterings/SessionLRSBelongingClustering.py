from src.userempathetic.clustering.clusterings.Clustering import SessionClustering
import numpy as np
from sklearn.cluster import DBSCAN
from src.userempathetic.utils.sqlUtils import sqlWrapper
from matplotlib import pyplot as plt


class SessionLRSBelongingClustering(SessionClustering):
    #tablename = 'sessionlrsbelongingclusters'
    #sqlWrite = 'INSERT INTO '+tablename+ ' (user_id,histogram,count) VALUES (%s,%s,%s)'

    def __init__(self, clusterExtractor):
        SessionClustering.__init__(self)
        self.clusterExtractor = clusterExtractor
        self.clusteredData = dict()
        self.n_clusters = 0
        self.clusteringAlgorithm = DBSCAN(eps=0.3, min_samples=2,metric='manhattan')
        self.featuresDIM = 0
    #TODO: definir metodo generico para el ClusterExtractor a partir de esto.
    def clusterize(self):
        sqlFT = sqlWrapper(db='FT')
        ids = list()
        sqlRead = ('select session_id,vector from sessionlrsbelongingfeatures')
        rows= sqlFT.read(sqlRead)
        assert len(rows)>0
        X = list()
        for row in rows:
            ids.append(int(row[0]))
            X.append([int(x) for x in row[1].split(' ')])
        self.featuresDIM = len(X[0]) # Dimension of feature vector.
        #print(X)

        ##############################################################################
        # Compute DBSCAN
        self.clusteringAlgorithm.fit(X)

        core_samples_mask = np.zeros_like(self.clusteringAlgorithm.labels_, dtype=bool)
        core_samples_mask[self.clusteringAlgorithm.core_sample_indices_] = True
        labels = self.clusteringAlgorithm.labels_

        #print(labels)

        unique_labels = set(labels)

        #print(core_samples_mask)
        for k in unique_labels:
            #   print('LABEL=' + str(k))
            if k == -1:
            #print('k=' + str(k)+' is noise...')
                pass
            else:
                class_member_mask = (labels == k)
                xy=[x for x,i,j in zip(X,class_member_mask,core_samples_mask) if i & j]
                self.clusteredData[k]=xy

        # Number of clusters in labels, ignoring noise if present.
        self.n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        self.printClusters()

    def visualizeClusters(self):
        if self.n_clusters > 1:
            f, ax = plt.subplots(self.n_clusters, sharex=True, sharey=True)

            # Fine-tune figure; make subplots close to each other and hide x ticks for
            # all but bottom plot.
            f.subplots_adjust(hspace=0)
            plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
            for k,v in self.clusteredData.items():
                low = self.getMin(v)
                c = self.getCentroid(v)
                up = self.getMax(v)
                idx = range(self.featuresDIM)
                ax[k].plot(idx,low,'g.')
                ax[k].plot(idx,up,'r.')
                ax[k].plot(idx,c,'b.',markersize=10)

            plt.xlim([-0.2,self.featuresDIM-1+0.2])
            plt.yticks([0, 1])
            plt.margins(0.2)
            plt.xlabel("LRSs index.")
            ax[self.n_clusters/2].set_ylabel("Utilización del LRS")
            ax[0].set_title("Uso de LRSs por sesión representativa de cada cluster")
            plt.show()

    def printClusters(self):
        print('Estimated number of clusters: %d' % self.n_clusters)
        for k,v in self.clusteredData.items():
            print("Cluster "+ str(k)+",\t"+str(len(v))+" elementos:\n"+ str(v))

