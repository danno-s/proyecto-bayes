#!/usr/bin/python

import json
import mysql.connector
from phpserialize import *

with open('connections.json', 'r') as f:
    connectionsJSON = f.read()

connections = json.loads(connectionsJSON)

connRead = connections[0]
connWrite = connections[1]

sqlRead = 'select distinct variables from pageview'
cnx = mysql.connector.connect(user=connRead['user'], password=connRead['passwd'], host=connRead['host'],database=connRead['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
rows = cursor.fetchall()

L = set()
# Leer datos serializados de usuario: ID, Nombre de usuario y Perfil
for row in rows:
    l = loads(bytes(row[0], 'UTF-8'))
    try:
        username = l[b'username'].decode("utf-8")
        user_id = int(l[b'id_usuario'].decode("utf-8"))
        perfil = l[b'perfil'].decode("utf-8")
        L.add((user_id, username, perfil))
    except KeyError:
        print("No se encontraron datos de usuario en la columna \'variables\'.")
        break
    except TypeError:
        print("Texto no corresponde a datos de usuario, variable leida = "+str(l))

cnx.close()
print(L)
if len(L) is not 0:
    cnx = mysql.connector.connect(user=connWrite['user'], password=connWrite['passwd'], host=connWrite['host'],database=connWrite['db'])
    cursor = cnx.cursor()
    # Resetear users
    cursor.execute("TRUNCATE users")
    cnx.commit()
    # Guardar nueva info.
    sqlWrite = "INSERT INTO users (id_usuario,username,perfil) VALUES (%s, %s, %s)"
    for item in L:
        cursor.execute(sqlWrite,item)

    cnx.commit()
    cnx.close()
