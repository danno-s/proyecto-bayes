#!/usr/bin/python

from src.userempathetic.utils.sqlUtils import sqlWrapper



def consecutiveIdxs(idxs, repeat):
    """Genera tuplas de tamaño 'repeat' con los índices consecutivos extraidos de 'idxs'

    Parameters
    ----------
    idxs : [int]
        Lista de índices.
    repeat : int
        Tamaño de las tuplas de índices consecutivos

    Yields
    -------
    Tuple
        Las tuplas de índices consecutivos
    """
    for i in idxs[:-repeat + 1]:
        yield tuple(x for x in range(i, i + repeat))


def subsequences(iterable):
    """Generador de las subsecuencias posibles a partir de una sesión

    Parameters
    ----------
    iterable : iterable
        Objeto iterable de donde se generan las secuencias

    Yields
    -------
    str
        Las subsecuencias posibles
    """
    pool = tuple(iterable)
    n = len(pool)
    if n > 1:
        for r in range(2, n):
            inGen = (x for x in consecutiveIdxs(range(n), repeat=r))
            for indices in inGen:
                yield ' '.join(tuple(pool[i] for i in indices))

    yield ' '.join(pool)


def contains(shortest, longest):
    """Verifica si la subsecuencia 'shortest' esta contenida dentro de la subsecuencia 'longest'

    Parameters
    ----------
    shortest : string
        Subsecuencia más corta
    longest : string
        Subsecuencia más larga

    Returns
    -------
    bool
        True si shortest está contenido en longest, False si no está contenida o son iguales
    """
    if shortest == longest:
        return False
    for i in range(len(longest) - len(shortest) + 1):
        for j in range(len(shortest)):
            if longest[i + j] != shortest[j]:
                break
        else:
            return True
    return False


def isSubContained(item, iterable):
    """Verifica si una secuencia 'item' esta subcontenida dentro de algun elemento de la lista de secuencias 'iterable'

    Parameters
    ----------
    item : string
        La secuencia a buscar
    iterable : List
        La lista de secuencias en las que se busca

    Returns
    -------
    bool
        True si está contenida, False si no
    """
    for i, val in enumerate(iterable):
        if contains(item, val):
            return True
    return False


def getAllLRSs():
    """Permite obtener una lista con todas las secuencias LRS extraídas.

    Returns
    -------
    [string]
        Lista de secuencias LRS.
    """
    sqlCD = sqlWrapper('CD')
    sqlRead = 'select sequence from lrss'
    rows = sqlCD.read(sqlRead)
    assert len(rows) > 0
    return [item[0] for item in rows]


def getAllSessionIDs():
    """Obtiene una lista con las IDs de sesiones extraídas.
    Returns
    -------
    [int]

    """
    sqlCD = sqlWrapper('CD')
    sqlRead = 'select id from sessions'
    rows = sqlCD.read(sqlRead)
    assert len(rows) > 0
    return [item[0] for item in rows]

def getAllSimulSessionIDs():
    """Obtiene una lista con las IDs de sesiones simuladas.
    Returns
    -------
    [int]

    """
    sqlCD = sqlWrapper('CD')
    sqlRead = 'select id from simulsessions'
    rows = sqlCD.read(sqlRead)
    assert len(rows) > 0
    return [item[0] for item in rows]
