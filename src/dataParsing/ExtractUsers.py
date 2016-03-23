#!/usr/bin/python
import json
from src.utils.sqlUtils import sqlWrapper


def extractUsers():
    """Extrae los usuarios con ID única que están en la base de datos de captura.

    Returns
    -------

    """
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = 'select distinct variables from pageview'
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    L = set()

    # Leer datos serializados de usuario: ID, Nombre de usuario y Perfil
    for row in rows:
        l = json.loads(row[0])
        try:
            username = l['user']
            user_id = int(l['id_usuario'])
            profile = l['profile']
            L.add((user_id, username, profile))
        except KeyError:
            print("No se encontraron datos de usuario en la columna \'variables\'.")
            break
        except TypeError:
            print("Texto no corresponde a datos de usuario, variable leida = " + str(l))

    assert len(L) > 0
    #  print(L)

    sqlPD.truncate("users")  # Limpia la tabla
    sqlWrite = "INSERT INTO users (user_id,username,profile) VALUES (%s, %s, %s)"  # Guardar usuarios
    for item in L:
        sqlPD.write(sqlWrite, item)


if __name__ == '__main__':
    extractUsers()
