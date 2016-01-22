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


def parseSimulSession():
    try:
        sqlPD = sqlWrapper(db='PD')  # Asigna las bases de datos que se accederán

    except:
        raise

    # Obtener todos los usuarios registrados.
    sqlRead = 'select id_usuario from users'
    users = sqlPD.read(sqlRead)
    assert len(users)>0
    userL = [int(x[0]) for x in users]
    assert len(userL)>0

    # Leer datos capturados

    # Asociar todos los capturados a su timestamp y usuario respectivo.
    data = list()

    # for i,row in enumerate(pageview):
    #     vars = loads(bytes(row[1], 'UTF-8'))    # Cargar variables de usuario
    #     tstamp = int(row[2])    # Timestamp
    #     urlTree = row[0]    # Arbol de URLs
    #     try:
    #         user_id=int(vars[b'id_usuario'].decode("utf-8"))
    #         data.append((user_id, urlTree, tstamp))
    #     except (KeyError, TypeError):
    #         print("Dato número " + str(i)+ " no contiene información de usuario.")
    # assert len(data)>0

    # Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
    sessions = list()

    tlimit = Config().getValue(attr='session_tlimit',mode='INT')
    assert tlimit>=0

    sqlPD.truncate("sessions")
    sqlPD.truncate("sessiondata")

    sqlWrite1 = "INSERT INTO sessions (user,inittime,endtime) VALUES (%s,%s,%s)"
    sqlWrite2 = "INSERT INTO sessiondata (urls,date) VALUES (%s,%s)"

    for user_id in userL:
        sqlRead = 'select id_user, id_urltree, clickdate from simulated where id_user = ' + str(user_id)
        allUserData = sqlPD.read(sqlRead)

        allUserData= [(int(x[1]),int(x[2])) for x in allUserData] # obtener todos los accesos del usuario.
        assert len(allUserData)>0

        for i in allUserData:
            assert len(i)>0
        tprev = allUserData[0][1]   #tiempo del primer dato.
        initTime = datetime.fromtimestamp(tprev) # TODO: AGREGAR TIMEZONE
        url = str(allUserData[0][0])
        sessionData = list()    # datos de sesión actual.
        sessionData.append(url) # inicializa sesión actual

        for i, step in enumerate(allUserData[1:]):
            if step[1] - tprev <= tlimit:   # condición para mantenerse en sesión actual
                sessionData.append(str(step[0]))                 # Agregar datos a sesión actual
            else:
                endTime = datetime.fromtimestamp(tprev) # TODO: AGREGAR TIMEZONE
                sqlPD.write(sqlWrite1, (user_id,initTime.isoformat(' '),endTime.isoformat(' ')))  # guardar sesión actual del usuario
                try:
                    sqlPD.write(sqlWrite2, (str(' '.join(sessionData)), initTime.date().isoformat()))
                except TypeError:
                    print(type(str(' '.join(sessionData))))
                    print(type(initTime.date().isoformat()))
                sessionData.clear()
                sessionData.append(str(step[0]))     # inicializar nueva sesión
                initTime = datetime.fromtimestamp(step[1]) # TODO: AGREGAR TIMEZONE
            tprev = step[1]     # actualizar timestamp previo.

        else:
            endTime = datetime.fromtimestamp(tprev) # TODO: AGREGAR TIMEZONE
            sqlPD.write(sqlWrite1, (user_id,initTime.isoformat(' '),endTime.isoformat(' ')))  # guardar sesión actual del usuario
            try:
                sqlPD.write(sqlWrite2, (str(' '.join(sessionData)), initTime.date().isoformat()))
            except TypeError:
                print(type(sessionData[0]))
                print(type(initTime.date().isoformat()))
                exit()

    # assert len(sessions) > 0

    # ss = ((x[0],x[1],x[2].isoformat(' '),x[3].isoformat(' ')) for x in sessions)
    # for s in ss:
    #     print(s)
    #
    # # Guardar sesiones en tablas sessions y urlsessions
    #
    # # Resetear sessions y urlsessions
    # sqlPD.truncate("sessions")
    # sqlPD.truncate("sessiondata")
    #
    # sqlWrite = "INSERT INTO sessions (user,inittime,endtime) VALUES (%s,%s,%s)"
    # for session in sessions:
    #     sqlPD.write(sqlWrite, (session[0],session[2].isoformat(' '),session[3].isoformat(' ')))
    #
    # sqlWrite = "INSERT INTO sessiondata (urls,date) VALUES (%s,%s)"
    # for session in sessions:
    #     sqlPD.write(sqlWrite,(str(session[1]),session[2].date().isoformat()))

if __name__ == '__main__':
    parseSimulSession()