from matplotlib import pyplot as plt


class ClusterView:

    def __init__(self):
        pass

    def view(self,clusterExtractor):
        i = 0
        for clustering in clusterExtractor.userClusteringsL:
            if clustering in clusterExtractor.performedClusteringsL:
                clusters = clusterExtractor.userClusterD[clustering].getClusters()
                n = len(clusters)
                if n > 1:
                    f1, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f1.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f1.axes[:-1]], visible=False)
                    features_dim = clusters[0].features_dim
                    for k, v in clusters.items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                       yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
                                       capsize=3,
                                       markersize=8)

                        ax[k].text(1.01, 0.5, '#' + str(k),
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                        ax[k].text(1.05, 0.5, "  (" + str(v.size) + ")",
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='green', fontsize=10, rotation='horizontal')

                    n_outliers = clusterExtractor.userClusterD[clustering].n_outliers
                    plt.text(0.85, -0.2, "N° outliers = " + str(n_outliers),verticalalignment='center',
                             horizontalalignment='left',transform=ax[k].transAxes, color='red', fontsize=10,
                             rotation='horizontal',fontweight='bold')
                    plt.xlim([-0.2, features_dim - 1 + 0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n / 2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f1.suptitle(clustering.__name__)

        for clustering in clusterExtractor.sessionClusteringsL:
            if clustering in clusterExtractor.performedClusteringsL:
                clusters = clusterExtractor.sessionClusterD[clustering].getClusters()
                n = len(clusters)
                if n > 1:
                    f2, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                    i += 1
                    # Fine-tune figure; make subplots close to each other and hide x ticks for
                    # all but bottom plot.
                    f2.subplots_adjust(hspace=0)
                    plt.setp([a.get_xticklabels() for a in f2.axes[:-1]], visible=False)
                    features_dim = clusters[0].features_dim
                    for k, v in clusters.items():
                        low = v.getMin()
                        c = v.getCentroid()
                        up = v.getMax()
                        idx = range(features_dim)
                        ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                       yerr=[[x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
                                       capsize=3,
                                       markersize=8)
                        ax[k].text(1.01, 0.5, '#' + str(k),
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='red', fontsize=10, fontweight='bold', rotation='horizontal')
                        ax[k].text(1.05, 0.5, "  (" + str(v.size) + ")",
                                   verticalalignment='center', horizontalalignment='left',
                                   transform=ax[k].transAxes,
                                   color='green', fontsize=10, rotation='horizontal')

                    n_outliers = clusterExtractor.sessionClusterD[clustering].n_outliers
                    plt.text(0.85, -0.2, "N° outliers = " + str(n_outliers),verticalalignment='center',
                             horizontalalignment='left',transform=ax[k].transAxes, color='red', fontsize=10,
                             rotation='horizontal',fontweight='bold')
                    plt.xlim([-0.2, features_dim - 1 + 0.2])
                    plt.yticks([0, 1])
                    plt.margins(0.2)
                    plt.xlabel(clustering.xlabel)
                    ax[n / 2].set_ylabel(clustering.ylabel)
                    ax[0].set_title(clustering.title)
                    f2.suptitle(clustering.__name__)
        plt.show()