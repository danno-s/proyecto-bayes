from matplotlib import pyplot as plt
from src.utils.clusteringUtils import getPerformedUserClusterings, \
    getPerformedSessionClusterings, getUserClusters, getSessionClusters, \
    getUserOutliersIDs, getSessionOutliersIDs


class ClusterView(object):
    """
    Clase encargada de mostrar una visualizacion de los distintos clusters
    obtenidos en el sistema. Obtiene los datos desde bases de datos y muestra
    un core sample promedio, maximo y minimo segun cada variable.
    """

    def __init__(self):

        self.user_clustering_dict = dict()
        self.session_clustering_dict = dict()

        for user_c in getPerformedUserClusterings():
            self.user_clustering_dict[user_c] = getUserClusters(user_c)

        for performed_c in getPerformedSessionClusterings():
            self.session_clustering_dict[performed_c] = \
                    getSessionClusters(performed_c)

    def _set_errorbar(self, axis, idx, low, mid, up):
        axis.errorbar(
            idx,
            mid,
            fmt="b.",
            ecolor="r",
            yerr=[
                [x - y for x, y in zip(mid, low)],
                [x - y for x, y in zip(up, mid)]],
            capsize=3,
            markersize=8)

    def _set_text(self, axis, k, v):
        axis.text(
            1.01,
            0.5,
            '#' + str(k),
            verticalalignment='center',
            horizontalalignment='left',
            transform=axis.transAxes,
            color='red',
            fontsize=10,
            fontweight='bold',
            rotation='horizontal')
        axis.text(
            1.05,
            0.5,
            "  (" + str(v.size) + ")",
            verticalalignment='center',
            horizontalalignment='left',
            transform=axis.transAxes,
            color='green',
            fontsize=10,
            rotation='horizontal')

    def _set_plt(self, clustering, fig, axis, n_outliers, features_dim):
        plt.text(
            0.85,
            -0.2,
            "N outliers = " + str(n_outliers),
            verticalalignment='center',
            horizontalalignment='left',
            transform=axis.transAxes,
            color='red',
            fontsize=10,
            rotation='horizontal',
            fontweight='bold')
        plt.xlim([-0.2, features_dim - 1 + 0.2])
        plt.yticks([0, 1])
        plt.margins(0.2)
        plt.xlabel(clustering.xlabel)


    def view_cluster(self, cluster_dict, outliersId_fun):
        """
        Dibuja en pyplot un diccionario de con clusters.

        Parameters
        ----------
        cluster_dict: Dictionary
        Un diccionario con clusters.
        """
        plot_count = 0
        for clustering in cluster_dict.keys():
            cluster = cluster_dict[clustering]
            len_cd = len(cluster)
            if len_cd <= 1:
                break

            fig, axis = plt.subplots(len_cd, sharex=True, sharey=True,\
                num=plot_count)

            plot_count += 1

            fig.subplots_adjust(hspace=0)
            plt.setp(
                [a.get_xticklabels() for a in fig.axes[:-1]],
                visible=False)

            features_dim = cluster[0].features_dim
            last_k = None
            for k, v in cluster.items():
                low = v.getMin()
                mid = v.getCentroid()
                up = v.getMax()
                idx = range(features_dim)

                try:
                    self._set_errorbar(axis[k], idx, low, mid, up)
                    self._set_text(axis[k], k, v)
                except IndexError as error:
                    print(error, k)

                last_k = k

            try:
                outliers = outliersId_fun(clustering)
                n_outliers = len(outliers)
                self._set_plt(clustering, fig, axis[last_k], n_outliers, \
                    features_dim)
                index = int(len_cd / 2)
                axis[index].set_ylabel(clustering.ylabel)
                axis[0].set_title(clustering.title)

                fig.suptitle(clustering.__name__)
            except IndexError as error:
                print(error, k)
        plt.show()

    def view(self):
        """
        Utiliza modulo pyplot de matplotlib para graficar el valor por
        variable del centroide, maximo y minimo de cada cluster.
        Para cada tipo de clustering realizado tanto para usuarios como
        sesiones.

        Returns
        -------

        """
        self.view_cluster(self.user_clustering_dict, getUserOutliersIDs)
        self.view_cluster(self.session_clustering_dict, getSessionOutliersIDs)

if __name__ == '__main__':
    cv = ClusterView()
    cv.view()
