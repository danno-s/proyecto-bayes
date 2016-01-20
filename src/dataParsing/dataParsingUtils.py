#!/usr/bin/python

"""
Módulo contiene funciones usadas por otros scripts
"""
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

    pass
