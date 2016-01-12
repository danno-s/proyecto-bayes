#!/usr/bin/python

import json
import mysql.connector
from phpserialize import *
tlimit = 10

def indexinsert(l, t):

    for i in range(len(l)):
        if l[i][1] > t :
            return i
    return len(l)

def insession(t, tinit, tend):

    if tinit <= t <= tend:
        return True
    else:
        return False


with open('connections.json', 'r') as f:
    connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connGC = connections[0]
connPD = connections[1]


cnx = mysql.connector.connect(user=connPD['user'], password=connPD['passwd'], host=connPD['host'],database=connPD['db'])
cursor = cnx.cursor()

sqlRead = 'select id_usuario from users'
cursor.execute(sqlRead)
users = cursor.fetchall()
userL = list()
for row in users:
    userL.append(row[0])
cnx.close()

data = dict()

sqlRead = 'select urls, variables, clickDate from pageview'
cnx = mysql.connector.connect(user=connGC['user'], password=connGC['passwd'], host=connGC['host'],database=connGC['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
pageview = cursor.fetchall()

for row in pageview:
    vars = loads(bytes(row[1], 'UTF-8'))
    tstamp = int(row[2])
    urlTree = row[0]
    try:
        user_id=int(vars[b'id_usuario'].decode("utf-8"))
        data[user_id] =(urlTree,tstamp)
    except (KeyError, TypeError):
        break

# Acceder a tstamp del usuario 824 => print(data[824][1])
sessions = list()

for id in userL:    # Por cada usuario registrado hacer query buscando los datos de su sesión:
    sqlRead = "select MIN(clickDate) from pageview where variables like \'%"+str(id)+"%\'"
    cursor.execute(sqlRead)
    tinit=cursor.fetchall()[0][0]  # Obtener todos los datos capturados para ese usuario.
    flag = True
    sessionData = list()
    while flag:
        sqlRead = "select urls from pageview where variables like \'%"+str(id)+"%\' AND clickDate between " +str(tinit)+" and "+ str(tinit+tlimit)
        cursor.execute(sqlRead)
        data = cursor.fetchall()    # Colección de datos dentro de una sesión.
        sessionData.append(data)
        if len(data) is 0:
            flag = False
            break
        tinit = tinit+tlimit+1  # TODO: PROBLEMA ACÁ!
        openSession = False
    sessions.append((id,sessionData))
# "select urls,clickDate from pageview where variables like \'%"+str(id)+"%\' AND clickDate - "+ tINIT +"< "+tlimit

'''
for id in userL:    # Por cada usuario registrado hacer query buscando los datos de su sesión:
    sqlRead = "select urls,clickDate from pageview where variables like \'%"+str(id)+"%\'"
    cursor.execute(sqlRead)
    rows=cursor.fetchall()  # Obtener todos los datos capturados para ese usuario.
    tinit = rows[0][1]      # Tiempo inicial de primera sesión
    sessionData = list()    # Colección de datos dentro de una sesión.
    openSession = False
    for step in rows:           # Hasta que se acaben datos del usuario, extraer todas las sesiones
        print("tNOW in sesion? "+str(step[1] - tinit < tlimit))
        if step[1] - tinit < tlimit:
            print("UserID= "+str(id)+" Cantidad de nodos: "+str(len(sessionData)))
            sessionData.append(step[0])
            openSession = True
        else:
            openSession = False
        if not openSession:
            sessions.append((id,sessionData))    # Almacenar una sesión con su usuario.
            print("N° de sesiones registradas: "+ str(len(sessions)))
            sessionData.clear()
            tinit = step[1]+1                     # Reiniciar contador y tiempo final.
'''


for session in sessions:
    print(session)
cnx.close()


#for key,val in userSessions.items():
#    print(str(key)+str(val))

# for key in D.keys():
#     D[key] = str(tuple(D[key]))
#
# print(D)
#
# sqlWrite = ("INSERT INTO userclusteringfeatures (id_usuario,userFeatureVector) VALUES (%s, %s)")
#
# for item in D.items():
# 	cursor.execute(sqlWrite,item)
#
# cnx.commit()
# cnx.close()