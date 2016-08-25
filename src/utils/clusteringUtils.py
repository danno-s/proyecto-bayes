import itertools

from src.utils.sqlUtils import sqlWrapper
from src.clusterClass.Cluster import Cluster


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
    """Metodo de prueba para combinar clusters de usuarios obtenidos con distintas caracteristicas en un unico
    cluster de usuario.

    Parameters
    ----------
    cE : ClusterExtractor
        un ClusterExtractor con clusters ya calculados.

    Returns
    -------

    """
    from src.clustering.clusterings.userclusterings.UserMacroStatesBelongingClustering import UserMacroStatesBelongingClustering
    from src.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering

    userClustersL1 = [x.ids for x in cE.userClusterD[
        UserLRSHistogramClustering].values()]
    userClustersL2 = [x.ids for x in cE.userClusterD[
        UserMacroStatesBelongingClustering].values()]
    clusteringIntersections(userClustersL1, userClustersL2)


def clusteringIntersections(clustersL1, clustersL2):
    """Calcula elementos de la interseccion entre dos Clusters

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
    """Obtiene una lista con las id de los macro estados desde la base de datos

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
    sqlRead = "select cluster_id,members from userclusters where clustering_name = '" + \
        clustering_name + "'"
    rows = sqlCL.read(sqlRead)
    userClustersD = dict()
    for row in rows:
        userClustersD[int(row[0])] = [int(x) for x in row[1].split(' ')]
    return userClustersD


def getPerformedUserClusterings():
    """Obtiene una lista con los clusterings de usuarios que fueron realizados correctamente.

    Returns
    -------
    list
        lista de clusterings de usuario realizados.

    """
    from src.utils.loadConfig import Config
    sqlCL = sqlWrapper('CL')
    performedClusteringsL = list()

    sqlRead = 'SELECT DISTINCT clustering_name FROM userclusters WHERE cluster_id IS NOT NULL'
    rows = sqlCL.read(sqlRead)
    for row in rows:
        performedClusteringsL.append(Config.userClusteringsD[row[0]])

    return performedClusteringsL


def getPerformedSessionClusterings():
    """Obtiene una lista con los clusterings de sesiones que fueron realizados correctamente.

    Returns
    -------
    list
        lista de clusterings de sesiones realizados.

    """
    from src.utils.loadConfig import Config
    sqlCL = sqlWrapper('CL')
    performedClusteringsL = list()

    sqlRead = 'SELECT DISTINCT clustering_name FROM sessionclusters WHERE cluster_id IS NOT NULL'
    rows = sqlCL.read(sqlRead)
    for row in rows:
        performedClusteringsL.append(Config.sessionClusteringsD[row[0]])

    return performedClusteringsL


def getVectorsOfUserCluster(cl_id):
    """ Retorna lista de vectores para cluster de usuario de ID cl_id

    Parameters
    ----------
    cl_id: id del cluster

    Returns
    -------
    list
        lista de vectores de cluster de usuario de ID cl_id.
    """
    sqlCL = sqlWrapper('CL')
    rows = sqlCL.read(
        "SELECT vectors FROM userclusters WHERE id = " + str(cl_id))
    return rows[0][0]


def getVectorsOfSessionCluster(cl_id):
    """ Retorna lista de vectores para cluster de sesion de ID cl_id

    Parameters
    ----------
    cl_id: id del cluster

    Returns
    -------
    list
        lista de vectores de cluster de sesion de ID cl_id.
    """
    sqlCL = sqlWrapper('CL')
    rows = sqlCL.read(
        "SELECT vectors FROM sessionclusters WHERE id = " + str(cl_id))
    return rows[0][0]


def getUserClusterLabels(clustering):
    """ Retorna una lista con las etiquetas de todos los clusters obtenidos para el clustering indicado.

    Parameters
    ----------
    clustering: UserClustering
        clustering de Usuario

    Returns
    -------
    list
        lista de int con etiquetas de clusters obtenidos en el clustering indicado.
    """
    sqlCL = sqlWrapper('CL')
    rows = sqlCL.read("SELECT DISTINCT cluster_id FROM userclusters WHERE clustering_name = '" +
                      str(clustering.__name__[:-10]) + "' AND cluster_id != -1")
    L = list()
    for row in rows:
        L.append(row[0])
    return L


def getSessionClusterLabels(clustering):
    """ Retorna una lista con las etiquetas de todos los clusters obtenidos para el clustering indicado.

    Parameters
    ----------
    clustering: SessionClustering
        clustering de sesion

    Returns
    -------
    list
        lista de int con etiquetas de clusters obtenidos en el clustering indicado.
    """
    sqlCL = sqlWrapper('CL')
    rows = sqlCL.read("SELECT DISTINCT cluster_id FROM sessionclusters WHERE clustering_name = '" +
                      str(clustering.__name__[:-10]) + "' AND cluster_id != -1")
    L = list()
    for row in rows:
        L.append(row[0])
    return L


def getSessionOutliersIDs(clustering):
    """ Retorna una lista con las IDs de todos los outliers obtenidos para el clustering indicado.

    Parameters
    ----------
    clustering: SessionClustering
        clustering de sesion

    Returns
    -------
    list
        lista de int con IDs de outliers obtenidos en el clustering indicado.
    """
    sqlCL = sqlWrapper('CL')
    rows = sqlCL.read("SELECT members FROM sessionclusters WHERE clustering_name = '" +
                      str(clustering.__name__[:-10]) + "' AND cluster_id = -1")
    L = list()
    for row in rows:
        for x in row[0].split(' '):
            L.append(int(x))
    return L


def getUserOutliersIDs(clustering):
    """ Retorna una lista con las IDs de todos los outliers obtenidos para el clustering indicado.

    Parameters
    ----------
    clustering: UserClustering
        clustering de usuario

    Returns
    -------
    list
        lista de int con IDs de outliers obtenidos en el clustering indicado.
    """
    sqlCL = sqlWrapper('CL')
    rows = sqlCL.read("SELECT members FROM userclusters WHERE clustering_name = '" +
                      str(clustering.__name__[:-10]) + "' AND cluster_id = -1")
    L = list()
    for row in rows:
        for x in row[0].split(' '):
            L.append(int(x))
    return L


def getUserClusters(clustering):
    """ Retorna un diccionario con los clusters obtenidos para el clustering indicado.

    Parameters
    ----------
    clustering: UserClustering
        clustering de usuario

    Returns
    -------
    dict
        diccionario de clusters obtenidos para el clustering indicado.
    """
    sqlCL = sqlWrapper('CL')
    labels = getUserClusterLabels(clustering)
    userClusterD = dict()
    for k in labels:
        rows = sqlCL.read("SELECT members,vectors FROM userclusters WHERE clustering_name = '" +
                          str(clustering.__name__[:-10]) + "' AND cluster_id = " + str(k))
        for row in rows:
            ids = [int(x) for x in row[0].split(' ')]
            vectors = [[float(y) for y in x.split(' ')]
                       for x in row[1].split(';')]
            userClusterD[k] = Cluster(
                ids=ids, vectors=vectors, label=k, clusteringType=clustering.__name__[:-10])
    return userClusterD


def getSessionClusters(clustering):
    """ Retorna un diccionario con los clusters obtenidos para el clustering indicado.

    Parameters
    ----------
    clustering: SessionClustering
        clustering de sesion

    Returns
    -------
    dict
        diccionario de clusters obtenidos para el clustering indicado.
    """
    sqlCL = sqlWrapper('CL')
    labels = getSessionClusterLabels(clustering)
    sessionClusterD = dict()
    for k in labels:
        rows = sqlCL.read("SELECT members,vectors FROM sessionclusters WHERE clustering_name = '" +
                          str(clustering.__name__[:-10]) + "' AND cluster_id = " + str(k))
        for row in rows:
            ids = [int(x) for x in row[0].split(' ')]
            vectors = [[float(y) for y in x.split(' ')]
                       for x in row[1].split(';')]
            sessionClusterD[k] = Cluster(
                ids=ids, vectors=vectors, label=k, clusteringType=clustering.__name__[:-10])
    return sessionClusterD

if __name__ == '__main__':
    #from src.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
    #a = getUserClusters(UserLRSHistogramClustering)
    # for k,v in a.items():
    #    print(str(k)+": "+str(v))
    pass
