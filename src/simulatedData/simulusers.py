#!/usr/bin/

"""

"""

import random
from src.utils.sqlUtils import sqlWrapper


def simulusers():
    n = 200

    usern = ["U8213221", "U6355477", "jefe_local"]
    user = [None]*n
    for i in range(n):
        user[i] = random.choice(usern)

    sqlPD = sqlWrapper(db='PD')

    id = random.sample(range(2000), n)
    perfil = random.sample(range(1000),n)

    L = list(zip(id,user,perfil))

    sqlPD.truncate("simusers")  # Limpia la tabla
    sqlWrite = "INSERT INTO simusers (id,username,perfil) VALUES (%s, %s, %s)" # Guardar usuarios
    for item in L:
        sqlPD.write(sqlWrite,item)


if __name__ == '__main__':
    simulusers()

