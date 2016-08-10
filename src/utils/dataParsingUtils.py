# -*- coding: utf-8 -*-

import hashlib

from src.utils.sqlUtils import sqlWrapper


def getMacroID(urls):
    """
    Obtiene el id en la base de datos de un arbol de urls

    Parameters
    ----------
    urls : str
        El arbol de urls a buscar
    Returns
    -------
    int
        El id del arbol de urls
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select id from urls where urls = '" + urls + "'"
    rows = sqlPD.read(sqlRead)
    return str(rows[0][0])


def getMicroID(contentElements):
    """
    Obtiene el id en la base de datos de un micro estado

    Parameters
    ----------
    contentElements : str
        El microestado a buscar
    Returns
    -------
    int
        El id del microestado
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select id from contentElements where raw = '" + contentElements + "'"
    rows = sqlPD.read(sqlRead)
    return str(rows[0][0])


def getProfileOf(user_id):
    """
    Obtiene el perfil del usuario con ID user_id

    Parameters
    ----------
    user_id : int
        El ID del usuario.
    Returns
    -------
    str
        el perfil del usuario.
    """
    sqlPD = sqlWrapper(db='PD')
    sqlRead = "select profile from users where user_id = " + str(user_id)
    rows = sqlPD.read(sqlRead)
    return rows[0][0]


def getUserOfSession(session_id):
    """
    Obtiene el ID del usuario que realizo la sesion de ID session_id

    Parameters
    ----------
    session_id : int
        El ID de la sesion.
    Returns
    -------
    int
        int con el ID del usuario.
    """
    try:
        sqlCD = sqlWrapper(db='CD')
    except:
        raise
    sqlRead = "select user_id from sessions where id = " + str(session_id)
    rows = sqlCD.read(sqlRead)
    return rows[0][0]


def getAllUserIDs():
    """
    Obtiene una lista con las id de los usuarios desde la base de datos

    Parameters
    ----------
    Returns
    -------
    list
        list de IDs de usuarios en forma de int
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select user_id from users"
    rows = sqlPD.read(sqlRead)
    return [int(row[0]) for row in rows]


def getAllSimulUserIDs():
    """
    Obtiene una lista con las id de los usuarios SIMULADOS desde la base de datos

    Parameters
    ----------
    Returns
    -------
    list
        list de IDs de usuarios en forma de int
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        print("excepcion con sql")
        raise
    sqlRead = "select user_id from users WHERE simulated = 1"
    rows = sqlPD.read(sqlRead)
    print("rows: "); print(rows)
    return [int(row[0]) for row in rows]


def getAllURLsIDs():
    """
    Obtiene una lista con las id de las urls desde la base de datos

    Parameters
    ----------
    Returns
    -------
    list
        list de IDs de urls en forma de int
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select id from urls"
    rows = sqlPD.read(sqlRead)
    return [int(row[0]) for row in rows]


def userStepsGen(user_id):
    """ Generador que permite obtener todos los nodos capturados del usuario indicado.

        Parameters
        ----------
        user_id : int
            id del usuario

        Yields
        ----------
        tuple
            (clickDate, urls_id, profile, micro_id)
        Returns
        -------

        """
    sqlCD = sqlWrapper('CD')
    rows = sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes WHERE user_id=" + str(user_id) +
                      " AND simulated = 0")
    for row in rows:
        # (clickDate, urls_id, profile, micro_id)
        yield (row[0], row[2], row[3], row[4])


def simulUserStepsGen(user_id):
    """ Generador que permite obtener solo los nodos simulados del usuario indicado.

        Parameters
        ----------
        user_id : int
            id del usuario

        Yields
        ----------
        tuple
            (clickDate, urls_id, profile, micro_id)
        Returns
        -------

        """
    sqlCD = sqlWrapper('CD')
    rows = sqlCD.read("SELECT clickDate,user_id,urls_id,profile,micro_id from nodes WHERE user_id=" + str(user_id) +
                      " AND simulated = 1")
    for row in rows:
        # (clickDate, urls_id, profile, micro_id)
        yield (row[0], row[2], row[3], row[4])

if __name__ == '__main__':
    a = userStepsGen(824)

    print(a.__next__())
    print(a.__next__())