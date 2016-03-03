#!/usr/bin/

"""

"""

import random
import numpy as np
import json
from src.userempathetic.utils.sqlUtils import sqlWrapper


def simulusers(n=200):
    """
    Genera usuarios simulados con un id, username y perfil

    Parameters
    ----------
    n : Int
        El número de usuarios simulados

    Returns
    -------
    list
        Lista de usuarios con id y perfil

    """
    usern = ["U8213221", "U6355477", "jefe_local"]  # usernames
    user = [None] * n
    for i in range(n):
        user[i] = random.choice(usern)

    user_id = random.sample(range(2000), n)  # ids generados al azar
    perfil = [0] * int(0.70 * n) + [1] * int(0.23 * n) + [2] * int(0.07 * n)  # perfiles de usuario
    random.shuffle(perfil)

    sqlPD = sqlWrapper(db='PD')
    sqlPD.truncate("users")  # Limpia la tabla
    sqlWrite = "INSERT INTO users (id_usuario,username,perfil) VALUES (%s, %s, %s)"  # Guardar usuarios

    for i in range(len(user_id)):
        sqlPD.write(sqlWrite, (user_id[i], user[i], perfil[i]))

    return list(zip(user_id, perfil))


def __vect(n):
    """
    Crea un vector de probabilidades de largo n/2

    Parameters
    ----------
    n : int
        El doble del largo del vector de probabilidades

    Returns
    -------
    Tuple
        La tupla con las probabilidades

    """
    v = [0] * int(n / 2)
    for i in range(len(v)):
        v[i] = 0.5 ** (i + 1)
    r = 1.0 - sum(v)
    if 1.0 > r:
        v[0] += r
    return tuple(v)


def __probtable(prob_list):
    """
    Crea un diccionario de largos de listas con sus vectores de probabilidades

    Parameters
    ----------
    prob_list : List
        La lista que contiene los largos de las listas

    Returns
    -------
    dict
        Diccionario con los largos y los vectores

    """
    lp = [0] * len(prob_list)
    for i in range(len(prob_list)):
        p = __vect(prob_list[i])
        if not p:
            p = [0]
        lp[i] = p

    return dict(zip(prob_list, lp))


def noise(lista, p):
    """
    Agrega ruido a una sesion

    Parameters
    ----------
    lista : List
        La sesión a la que se agregará ruido
    p : Dict
        La tabla de probabilidades segun la que se agrega el ruido

    Returns
    -------
    list
        La sesion con ruido
    """
    l = list(lista)
    if len(lista) <= 2:
        return l

    ins = np.random.multinomial(1, p[len(lista)], size=1).tolist()[0]  # numero de inserciones
    dele = np.random.multinomial(1, p[len(lista)], size=1).tolist()[0]  # numero de eliminaciones

    for i in range(ins.index(1)):
        l.insert(random.randint(0, len(l)), random.choice(l))

    for i in range(dele.index(1)):
        if len(l) > 1:
            l.pop(random.randint(0, len(l) - 1))

    return l


def getsession():
    """
    Selecciona las sesiones desde la tabla sessions

    Returns
    -------
    list
        Lista con las sesiones segun el perfil de usuario
    """
    sqlPD = sqlWrapper(db='CD')
    sqlRead = 'SELECT sequence from sessions'
    rows = sqlPD.read(sqlRead)
    lr = len(rows)

    L = [None] * 3

    if "," in rows[0][0]:
        L[0] = [y.split(' ') for y in [x[0] for x in rows[:int(lr * 0.7)]]]
        L[1] = [y.split(' ') for y in [x[0] for x in rows[int(lr * 0.7):int(lr * 0.94)]]]
        L[2] = [y.split(' ') for y in [x[0] for x in rows[int(lr * 0.94):]]]
    else:
        L[0] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[:int(lr * 0.7)]]]
        L[1] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[int(lr * 0.7):int(lr * 0.94)]]]
        L[2] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[int(lr * 0.94):]]]

    return L


def generate(configFile):
    """
    Genera los datos simulados y los guarda en la tabla simulatednodes

    Parameters
    ----------
    configFile : JSON
        Archivo de configuracion en formato JSON
    """
    users = simulusers(configFile["users"])
    session = getsession()
    prob = __probtable(list({len(x) for y in session for x in y if len(x) >= 3}))

    sqlCD = sqlWrapper(db='CD')
    sqlCD.truncate("simulatednodes")
    sqlWrite = "INSERT INTO simulatednodes (user_id, clickDate, urls_id,profile,micro_id,label) VALUES " \
               "(%s,%s,%s,%s,%s,%s)"

    for i in range(configFile["sessions"]):
        for u in users:
            l = session[u[1]]  # Se elige el grupo de sesiones de donde se seleccionara la session segun el perfil
            ses = random.choice(l)  # Se elige una sesion
            idx = l.index(ses)  # Se guarda su índice para poder etiquetar
            ses = noise(ses, prob)  # Se añade ruido
            if u[1] == 1:  # Se corrige la etiqueta
                idx += len(session[0])
            elif u[1] == 2:
                idx += len(session[0]) + len(session[1])
            d = random.randint(1450000000, 1462534931)  # Timestamp de inicio
            for s in ses:
                if type(s) is str:
                    url = [int(x) for x in s.split(",")]
                    L = [u[0], d, url[0], u[1], url[1], idx]
                else:
                    L = [u[0], d, s, u[1], None, idx]
                sqlCD.write(sqlWrite, L)  # Se guarda en la base de datos
                d += random.randint(1, configFile["time"] - 1)


if __name__ == '__main__':
    with open("simulConfig.json", "r") as f:
        file = f.read()
    generate(json.loads(file))
