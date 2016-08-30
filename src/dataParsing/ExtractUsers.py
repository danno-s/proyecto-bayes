#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from src.utils.sqlUtils import sqlWrapper

from src.utils.loadConfig import Config

capture_table = Config.getValue("capture_table")


def extractUsers():
    """Extrae los usuarios con ID unica que estan en la base de datos de captura.

    Returns
    -------

    """
    try:
        # Asigna las bases de datos que se accederan
        sqlGC = sqlWrapper(db='GC')
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    sqlRead = "select distinct variables from "+capture_table+" WHERE variables NOT LIKE 'null'"+\
              " AND variables NOT LIKE CONCAT('%',sha1('0'),'%')"

    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    L = set()

    # Leer datos serializados de usuario: ID, Nombre de usuario y Perfil
    for row in rows:
        l = json.loads(row[0])
        try:
            username = l['user']
            user_id = l['id_usuario']
            profile = l['profile']
            L.add((user_id, username, profile))
        except KeyError:
            print("\tNo se encontraron datos del usuario en la columna \'variables\'.")
            print("\t"+row[0])
            continue
        except TypeError:
            print("Texto no corresponde a datos de usuario, variable leida = " + str(l))

    assert len(L) > 0
    sqlReadAnon= "SELECT DISTINCT variables,IP FROM "+capture_table +" WHERE variables LIKE CONCAT('%',sha1('0'),'%')"
    rows = sqlGC.read(sqlReadAnon)

    for row in rows:
        l = json.loads(row[0])
        try:
            user_id = row[1]
            username = 'Anonymous'
            profile = l['profile']
            L.add((user_id, username, profile))
        except KeyError:
            print("No se encontraron datos de usuario en la columna \'variables\'.")
            continue
        except TypeError:
            print("Texto no corresponde a datos de usuario, variable leida = " + str(l))
    print("Total: "+str(len(L))+ " usuarios.")
    sqlPD.truncate("users")  # Limpia la tabla
    # Guardar usuarios
    sqlWrite = "INSERT INTO users (capture_userid,username,profile) VALUES (%s, %s, %s)"
    sqlPD.writeMany(sqlWrite, L)


if __name__ == '__main__':
    extractUsers()
