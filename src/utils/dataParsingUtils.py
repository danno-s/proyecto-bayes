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