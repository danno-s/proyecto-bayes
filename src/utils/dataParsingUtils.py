#!/usr/bin/python

"""
Módulo contiene funciones usadas por otros scripts
"""
import hashlib

from src.utils.sqlUtils import sqlWrapper
def getMacroID(urls):
    """
    Obtiene el id en la base de datos de un árbol de urls

    Parameters
    ----------
    urls : string
        El árbol de urls a buscar
    Returns
    -------
    int
        El id del árbol de urls
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select id_n from urls where urls = '"+urls+"'"
    rows = sqlPD.read(sqlRead)
    return str(rows[0][0])


def getMicroID(contentElements):
    """
    Obtiene el id en la base de datos de un micro estado

    Parameters
    ----------
    contentElements : string
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
    sqlRead = "select id from contentElements where raw = '"+contentElements+"'"
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
    string
        string con el perfil del usuario.
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select perfil from users where id_usuario = "+ str(user_id)
    rows = sqlPD.read(sqlRead)
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
    sqlRead = "select id_usuario from users"
    rows = sqlPD.read(sqlRead)
    return [int(row[0]) for row in rows]


def hash(string):
    """
    Retorna el valor hash de un string, usando MD5

    Parameters
    ----------
    string : string
        El string que se quiere convertir

    Returns
    -------
    string
        El valor del hash
    """
    return hashlib.md5(string.encode()).hexdigest()