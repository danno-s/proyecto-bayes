import itertools

from src.userempathetic.utils.sqlUtils import sqlWrapper


def intersectionIDs(clusterIDs1, clusterIDs2):
    """

    Parameters
    ----------
    clusterIDs1
        Lista de IDs de clusters
    clusterIDs2
        Lista de IDs de clusters
    Returns
    -------
        lista de elementos presentes en ambos clusters
    """
    return [val for val in clusterIDs1 if val in clusterIDs2]


def combineUserClusterings(cE):
    """Método de prueba para combinar clusters de usuarios obtenidos con distintas características en un único
    cluster de usuario.

    Parameters
    ----------
    cE : ClusterExtractor
        un ClusterExtractor con clusters ya calculados.

    Returns
    -------

    """
    from src.userempathetic.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
    from src.userempathetic.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering

    userClustersL1 = [x.ids for x in cE.userClusterD[UserLRSHistogramClustering].values()]
    userClustersL2 = [x.ids for x in cE.userClusterD[UserURLsBelongingClustering].values()]
    clusteringIntersections(userClustersL1, userClustersL2)


def clusteringIntersections(clustersL1, clustersL2):
    """Calcula elementos de la intersección entre dos Clusters

    Parameters
    ----------
    clustersL1 : list
        Elementos del cluster 1
    clustersL2 : list
        Elementos del cluster 2
    Returns
    -------

    """
    pairs = [x for x in itertools.product(clustersL1, clustersL2)]
    for pair in pairs:
        inter = intersectionIDs(pair[0], pair[1])
        n_intersected = len(inter)
        if n_intersected > 0:
            print(pair)
            print("Intersected Items: " + str(n_intersected))
            print(inter)


def getAllUserClusters(clustering_name):
    """Obtiene una lista con las id de las urls desde la base de datos

    Parameters
    ----------
    clustering_name : str
        Nombre de la tabla correspondiente al tipo de User Clusters que se desea obtener.
    Returns
    -------
    dict
        dict de clusters, donde cada elemento tiene todas las IDs de usuario pertenecientes a ese cluster.
    """
    try:
        sqlCL = sqlWrapper(db='CL')
    except:
        raise
    sqlRead = "select cluster_id,members from userclusters where clustering_name = '" + clustering_name + "'"
    rows = sqlCL.read(sqlRead)
    userClustersD = dict()
    for row in rows:
        userClustersD[int(row[0])] = [int(x) for x in row[1].split(' ')]
    return userClustersD
