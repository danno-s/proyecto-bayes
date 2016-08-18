from matplotlib import pyplot as plt
from src.utils.clusteringUtils import *


class ClusterView:
    """ Clase encargada de mostrar una visualizacion de los distintos clusters obtenidos en el sistema.
    Obtiene los datos desde bases de datos y muestra un core sample promedio, maximo y minimo segun cada variable.
    """

    def __init__(self):

        self.userClusteringD = dict()
        self.sessionClusteringD = dict()
        for uc in getPerformedUserClusterings():
            self.userClusteringD[uc] = getUserClusters(uc)
        for pc in getPerformedSessionClusterings():
            self.sessionClusteringD[uc] = getSessionClusters(pc)

    def view(self):
        """ Utiliza modulo pyplot de matplotlib para graficar el valor por variable del centroide, maximo y minimo de
        cada cluster, Para cada tipo de clustering realizado tanto para usuarios como sesiones.

        Returns
        -------

        """
        i = 0
        for clustering in self.userClusteringD.keys():
            clusterD = self.userClusteringD[clustering]
            n = len(clusterD.keys())
            if n > 1:
                f1, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                i += 1
                # Fine-tune figure; make subplots close to each other and hide x ticks for
                # all but bottom plot.
                f1.subplots_adjust(hspace=0)
                plt.setp([a.get_xticklabels()
                          for a in f1.axes[:-1]], visible=False)
                features_dim = clusterD[0].features_dim
                for k, v in clusterD.items():
                    low = v.getMin()
                    c = v.getCentroid()
                    up = v.getMax()
                    idx = range(features_dim)
                    ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                   yerr=[
                                       [x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
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

                outliers = getUserOutliersIDs(clustering)
                n_outliers = len(outliers)
                plt.text(0.85, -0.2, "N outliers = " + str(n_outliers), verticalalignment='center',
                         horizontalalignment='left', transform=ax[k].transAxes, color='red', fontsize=10,
                         rotation='horizontal', fontweight='bold')
                plt.xlim([-0.2, features_dim - 1 + 0.2])
                plt.yticks([0, 1])
                plt.margins(0.2)
                plt.xlabel(clustering.xlabel)
                ax[n / 2].set_ylabel(clustering.ylabel)
                ax[0].set_title(clustering.title)
                f1.suptitle(clustering.__name__)

        for clustering in self.sessionClusteringD.keys():
            clusterD = self.sessionClusteringD[clustering]
            n = len(clusterD.keys())
            if n > 1:
                f2, ax = plt.subplots(n, sharex=True, sharey=True, num=i)
                i += 1
                # Fine-tune figure; make subplots close to each other and hide x ticks for
                # all but bottom plot.
                f2.subplots_adjust(hspace=0)
                plt.setp([a.get_xticklabels()
                          for a in f2.axes[:-1]], visible=False)
                features_dim = clusterD[0].features_dim
                for k, v in clusterD.items():
                    low = v.getMin()
                    c = v.getCentroid()
                    up = v.getMax()
                    idx = range(features_dim)
                    ax[k].errorbar(idx, c, fmt='b.', ecolor='r',
                                   yerr=[
                                       [x - y for x, y in zip(c, low)], [x - y for x, y in zip(up, c)]],
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

                outliers = getSessionOutliersIDs(clustering)
                n_outliers = len(outliers)
                plt.text(0.85, -0.2, "N outliers = " + str(n_outliers), verticalalignment='center',
                         horizontalalignment='left', transform=ax[k].transAxes, color='red', fontsize=10,
                         rotation='horizontal', fontweight='bold')
                plt.xlim([-0.2, features_dim - 1 + 0.2])
                plt.yticks([0, 1])
                plt.margins(0.2)
                plt.xlabel(clustering.xlabel)
                index = int(n/2)
                ax[index].set_ylabel(clustering.ylabel)
                ax[0].set_title(clustering.title)
                f2.suptitle(clustering.__name__)
        plt.show()

if __name__ == '__main__':
    cv = ClusterView()
    cv.view()
