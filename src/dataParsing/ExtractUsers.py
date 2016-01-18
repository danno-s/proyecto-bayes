#!/usr/bin/python

"""
Extrae los usuarios diferentes en la base de datos
"""

import json
from phpserialize import *
from src.utils.sqlUtils import sqlWrapper


sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
sqlPD = sqlWrapper(db='PD')

sqlRead = 'select distinct variables from pageview'
rows = sqlGC.read(sqlRead)

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

#  print(L)

if len(L) is not 0:
    sqlPD.truncate("users")  # Limpia la tabla
    sqlWrite = "INSERT INTO users (id_usuario,username,perfil) VALUES (%s, %s, %s)" # Guardar usuarios
    for item in L:
        sqlPD.write(sqlWrite,item)

