#!/usr/bin/python

import json
import mysql.connector
from phpserialize import *
import os


with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
    connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0]
connPD = connections[1]

def getIDof(urls):
    cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
    cursor = cnx.cursor()
    # Obtener todos los usuarios registrados.
    sqlRead = "select id from urls where urls = \'" + str(urls)+"\'"
    print(sqlRead)
    cursor.execute(sqlRead)
    rows = cursor.fetchall()
    cnx.close()
    print(rows)
    return rows[0]


cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()
# Obtener todos los usuarios registrados.
sqlRead = 'select id_usuario from users'
cursor.execute(sqlRead)
users = cursor.fetchall()
userL = list()
for row in users:
    userL.append(row[0])
cnx.close()

# Leer datos capturados
sqlRead = 'select urls, variables, clickDate from pageview'
cnx = mysql.connector.connect(user=connGC['user'], password=connGC['passwd'], host=connGC['host'],database=connGC['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
pageview = cursor.fetchall()


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

print(getIDof(data[156][1]))
'''
sessions = list()
# Extraer sesiones para cada usuario, dado un tiempo limite entre pasos.
tlimit = 600    # Tiempo limite en segundos.

for user_id in userL:
    allUserData= [(x[1],x[2]) for x in data if x[0] == user_id] # obtener todos los accesos del usuario.
    tprev = allUserData[0][1]   #tiempo del primer dato.
    url = allUserData[0][0]
    sessionData = list()    # datos de sesión actual.
    sessionData.append(url) # inicializa sesión actual
    for i, step in enumerate(allUserData[1:]):
        if step[1] - tprev <= tlimit:   # condición para mantenerse en sesión actual
            sessionData.append(getIDof(step[0]))                 # Agregar datos a sesión actual
        else:
            sessions.append((user_id, sessionData.copy()))  # guardar sesión actual del usuario
            sessionData.clear()
            sessionData.append(getIDof(step[0]))     # inicializar nueva sesión
        tprev = step[1]     # actualizar timestamp previo.
    else:
        sessions.append((user_id,sessionData.copy()))   # guardar última sesión del usuario.

for session in sessions:
    print(session)
cnx.close()

# Guardar sesiones en tablas sessions y urlsessions

cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

# Resetear sessions y urlsessions
cursor.execute("TRUNCATE sessions")
cursor.execute("TRUNCATE urlsessions")

sqlWrite = ("INSERT INTO sessions (user) VALUES (")
for session in sessions:
    cursor.execute(sqlWrite + str(session[0])+")")
cnx.commit()

sqlWrite = ("INSERT INTO urlsessions (urls) VALUES (")
for session in sessions:
    cursor.execute(sqlWrite + '"'+ str(session[1]).replace('\"','\\"') + '"'+')')
cnx.commit()

cnx.close()
'''