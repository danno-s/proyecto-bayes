from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.utils.loadConfig import Config
from src.userempathetic.dataParsing.MicroStateVectorExtractor import MicroStateVectorExtractor
from src.userempathetic.nodeClass.MicroNode import MicroNode
from src.userempathetic.sessionClass.Session import Session

userFeaturesL = Config().getArray("user_features")  # lista de features de User extraídos.
sessionFeaturesL = Config().getArray("session_features")  # lista de features de Session extraídos.
elementTypes = MicroStateVectorExtractor().getElementTypes()  # lista de tipos de contentElements extraídos.

def getURLsTree(urls_id):
    """ Retorna un string en formato json correspondiente al árbol de URLs de la ID indicada.

    Parameters
    ----------
    urls_id : int
        ID de árbol de URLs deseado
    Returns
    -------
    str
        string de json con árbol de urls.
    """
    try:
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = "select urls from urls where id_n = " + str(urls_id)
    rows = sqlPD.read(sqlRead)
    return rows[0][0]

def getSession(session_id):
    """Retorna un objeto Session correspondiente a la sesión de ID indicada.

    Parameters
    ----------
    session_id : int
        ID de sesión deseada.

    Returns
    -------
    Session
        objeto Session con los datos de sesión cargados.
    """
    raw_session = getRawSessionData(session_id)
    sequence = raw_session[0].split(' ')
    if ',' not in raw_session[0]:
        session_type = 'macro'
        for i, macroid in enumerate(sequence):
            sequence[i] = (macroid, None)
    else:
        session_type = 'full'
        for i, pair in enumerate(sequence):
            pair = pair.split(',')
            sequence[i] = (pair[0], pair[1])
    profile = raw_session[1]
    user_id = int(raw_session[4])
    inittime = raw_session[2]
    endtime = raw_session[3]

    return Session(sequence, profile=profile, initTime=inittime, endTime=endtime, user_id=user_id,
                   session_id=session_id)


def getRawSessionData(session_id, sessionTable='sessions'):
    """Retorna datos "crudos" de la sesión indicada desde la tabla indicada (por defecto, 'sessions').

    Parameters
    ----------
    session_id : int
        ID de sesión.
    sessionTable : str
        nombre de la tabla de sesión a utilizar: 'sessions'(default) o 'simulsessions'

    Returns
    -------
    tuple
        (sequence,profile,inittime,endtime,user_id)
    """
    sqlCD = sqlWrapper('CD')
    row = sqlCD.read(
        "SELECT sequence,profile,inittime,endtime,user_id FROM " + sessionTable + " WHERE id = " + str(session_id))
    return row[0]


def getFeatureOfSession(session_id, feature):
    """Permite obtener el feature vector de una determinada sesión por su ID, para una caracterísitca específica.

    Parameters
    ----------
    session_id : int
        id de sesión
    feature:
        alguna clase que extienda a SessionFeature y haya sido utilizada por el FeatureExtractor.
    Returns
    -------
        [int]
            vector característica de la sesión.

    """
    assert feature in sessionFeaturesL
    sqlFT = sqlWrapper('FT')
    sqlRead = "SELECT vector FROM sessionfeatures WHERE session_id =" + str(session_id) +" AND feature_name = '"+feature+"'"
    row = sqlFT.read(sqlRead)
    if row[0][0] is None:
        return None
    else:
        return [int(x) for x in row[0][0].split(' ')]



def getMSS(s1, s2):
    """ Permite obtener los elementos comunes de cada sesión en forma de la máxima secuencia compartida.

    Parameters
    ----------
    s1 : Session
        una sesión.
    s2 ; Session
        una sesión.

    Returns
    -------
    [(int,int)]
        Indica la secuencia MSS de la sesión de menor largo.
    [(int,int)]
        Indica la secuencia MSS de la sesión de mayor largo.
    [int]
        Indica cantidad de nodos de sesiones saltados para encontrar correspondencia entre los elementos del MSS.
    """
    if len(s1.sequence) >= len(s2.sequence):
        shortest = s2.sequence
        largest = s1.sequence
    else:
        shortest = s1.sequence
        largest = s2.sequence

    v1 = list()
    v2 = list()
    c = list()  # Cuenta los nodos saltados para identificar una equivalencia de macroestado.

    ind1 = 0
    ind2 = 0
    count = 0
    for i in shortest:
        for j in largest[ind2:]:
            # print(str(i)+"|"+str(j))
            if i[0] == j[0]:
                v1.append(i)
                v2.append(j)
                c.append(count)
                ind2 += 1
                count = 0
                break
            else:
                count += 1
            ind2 += 1
        if len(v1) == 0:
            ind1 += 1
            ind2 = 0
            count = ind1

    return v1, v2, c


def getMicroNode(micro_id):
    """Permite obtener un objeto MicroNode que representa el microestado de un nodo.

    Parameters
    ----------
    micro_id : int
        ID del micro estado que se desea obtener como MicroNode.
    Returns
    -------
    MicroNode
        una instancia de MicroNode con los vectores de contentElements correspondientes.

    """
    sqlPD = sqlWrapper('PD')
    sqlRead = "SELECT * FROM contentElements WHERE id = " + str(micro_id)
    row = sqlPD.read(sqlRead)
    return MicroNode(row, key="")  # TODO: FIND OUT WTF IS key...


def getFeatureOfUser(user_id, feature):
    """Permite obtener el feature vector de un determinado usuario por su ID, para una caracterísitca específica.

    Parameters
    ----------
    user_id : int
        id de usuario
    feature:
        alguna clase que extienda a UserFeature y haya sido utilizada por el FeatureExtractor.
    Returns
    -------
        [int]
            vector característica del usuario.

    """
    assert feature in userFeaturesL
    sqlFT = sqlWrapper('FT')
    sqlRead = "SELECT vector FROM userfeatures WHERE user_id = " + str(user_id) +" AND feature_name = '"+feature+"'"
    row = sqlFT.read(sqlRead)
    if len(row) == 0 or row[0][0] is None:
        return None
    else:
        return [float(x) for x in row[0][0].split(' ')]

def getSimulSession(session_id):
    """Retorna un objeto Session correspondiente a la sesión simulada de ID indicada.

    Parameters
    ----------
    session_id : int
        ID de sesión deseada.

    Returns
    -------
    Session
        objeto Session con los datos de sesión cargados.
    """
    raw_session = getRawSessionData(session_id,sessionTable='simulsessions')
    sequence = raw_session[0].split(' ')
    if ',' not in raw_session[0]:
        session_type = 'macro'
        for i, macroid in enumerate(sequence):
            sequence[i] = (macroid, None)
    else:
        session_type = 'full'
        for i, pair in enumerate(sequence):
            pair = pair.split(',')
            sequence[i] = (pair[0], pair[1])
    profile = raw_session[1]
    user_id = int(raw_session[4])
    inittime = raw_session[2]
    endtime = raw_session[3]

    return Session(sequence, profile=profile, initTime=inittime, endTime=endtime, user_id=user_id,
                   session_id=session_id)


if __name__ == '__main__':
    #print(getMicroNode(12).toDict())
    print(getFeatureOfUser(1,'UserLRSHistogram'))
