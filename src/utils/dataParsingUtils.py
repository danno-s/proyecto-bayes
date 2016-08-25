# -*- coding: utf-8 -*-

from src.dataParsing.macroStateExtractors.CustomMacroStateExtractor import CustomMacroStateExtractor
from src.dataParsing.macroStateExtractors.URLsMacroStateExtractor import  URLsMacroStateExtractor
from src.utils.sqlUtils import sqlWrapper

macroStateExtractorsD = {"URLs": URLsMacroStateExtractor,
                         "Custom": CustomMacroStateExtractor}
import json


'''
def getMacroID(data):
    """
    Obtiene el id en la base de datos del macro estado

    Parameters
    ----------
    data: (url,urls,variables)
        La url principal a buscar, el arbol de urls a buscar y las variables de la captura.
    Returns
    -------
    int
        La id del macro estado.
    """
    msmapper = getMacroMapper()
    urlstr = data[0]
    if urlstr.endswith(' undefined'):
        urlstr = urlstr[:-10]
    res = msmapper.map((urlstr, data[1], data[2]))
    if res is not False and not isinstance(res, str):
        return res.getId()
    return False
'''


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
    if len(rows) is not 0:
        return str(rows[0][0])
    return False

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
    sqlRead = "select id from users WHERE simulated = 1"
    rows = sqlPD.read(sqlRead)
    print("rows: "); print(rows)
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
            (clickDate, macro_id, profile, micro_id)
        Returns
        -------

        """
    sqlCD = sqlWrapper('CD')
    rows = sqlCD.read("SELECT clickDate,user_id,macro_id,profile,micro_id from nodes WHERE user_id=" + str(user_id) +
                      " AND simulated = 0")
    for row in rows:
        # (clickDate, macro_id, profile, micro_id)
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
            (clickDate, macro_id, profile, micro_id)
        Returns
        -------

        """
    sqlCD = sqlWrapper('CD')
    rows = sqlCD.read("SELECT clickDate,user_id,macro_id,profile,micro_id from nodes WHERE user_id=" + str(user_id) +
                      " AND simulated = 1")
    for row in rows:
        # (clickDate, macro_id, profile, micro_id)
        yield (row[0], row[2], row[3], row[4])
