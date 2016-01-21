#!/usr/bin/python

"""
Extrae las distintas sesiones que existen en la base de datos
"""

from phpserialize import *
from datetime import datetime
from src.utils.sqlUtils import sqlWrapper
from src.utils.loadConfig import Config


def getIDof(urls):
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
    sqlRead = 'select id_n from urls where urls = '+ "'"+urls+"'"
    rows = sqlPD.read(sqlRead)
    return str(rows[0][0])


def parseSessions():
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')

    except:
        raise

    # Obtener todos los usuarios registrados.
    sqlRead = 'select id_usuario from users'
    users = sqlPD.read(sqlRead)
    assert len(users)>0
    userL = list()
    for row in users:
        userL.append(row[0])
    assert len(userL)>0

    # Leer datos capturados
    sqlRead = 'select urls, variables, clickDate from pageview'
    pageview = sqlGC.read(sqlRead)
    assert len(pageview)>0

    # Asociar todos los capturados a su timestamp y usuario respectivo.
    data = list()

    for i,row in enumerate(pageview):
        vars = loads(bytes(row[1], 'UTF-8'))    # Cargar variables de usuario
        tstamp = int(row[2])    # Timestamp
        urlTree = row[0]    # Arbol de URLs
        try:
            user_id=int(vars[b'id_usuario'].decode("utf-8"))
            data.append((user_id, urlTree, tstamp))
        except (KeyError, TypeError):
            print("Dato número " + str(i)+ " no contiene información de usuario.")
    assert len(data)>0

    # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
    sessions = list()

    tlimit = Config().getValue(attr='session_tlimit',mode='INT')
    assert tlimit>=0

    for user_id in userL:
        allUserData= [(x[1],x[2]) for x in data if x[0] == user_id] # obtener todos los accesos del usuario.
        assert len(allUserData)>0

        for i in allUserData:
            assert len(i)>0
        tprev = allUserData[0][1]   #tiempo del primer dato.
        initTime = datetime.fromtimestamp(tprev) # TODO: AGREGAR TIMEZONE
        url = allUserData[0][0]
        sessionData = list()    # datos de sesión actual.
        sessionData.append(getIDof(url)) # inicializa sesión actual

        for i, step in enumerate(allUserData[1:]):
            if step[1] - tprev <= tlimit:   # condición para mantenerse en sesión actual
                sessionData.append(getIDof(step[0]))                 # Agregar datos a sesión actual
            else:
                endTime = datetime.fromtimestamp(tprev) # TODO: AGREGAR TIMEZONE
                sessions.append((user_id, ' '.join(sessionData),initTime,endTime))  # guardar sesión actual del usuario
                sessionData.clear()
                sessionData.append(getIDof(step[0]))     # inicializar nueva sesión
                initTime = datetime.fromtimestamp(step[1]) # TODO: AGREGAR TIMEZONE
            tprev = step[1]     # actualizar timestamp previo.

        else:
            endTime = datetime.fromtimestamp(tprev) # TODO: AGREGAR TIMEZONE
            print(type(sessionData[0]))
            sessions.append((user_id,' '.join(sessionData),initTime,endTime))   # guardar última sesión del usuario.

    assert len(sessions) > 0

    ss = ((x[0],x[1],x[2].isoformat(' '),x[3].isoformat(' ')) for x in sessions)
    for s in ss:
        print(s)

    # Guardar sesiones en tablas sessions y urlsessions

    # Resetear sessions y urlsessions
    sqlPD.truncate("sessions")
    sqlPD.truncate("sessiondata")

    sqlWrite = "INSERT INTO sessions (user,inittime,endtime) VALUES (%s,%s,%s)"
    for session in sessions:
        sqlPD.write(sqlWrite, (session[0],session[2].isoformat(' '),session[3].isoformat(' ')))

    sqlWrite = "INSERT INTO sessiondata (urls,date) VALUES (%s,%s)"
    for session in sessions:
        sqlPD.write(sqlWrite,(str(session[1]),session[2].date().isoformat()))

if __name__ == '__main__':
    parseSessions()