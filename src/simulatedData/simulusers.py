#!/usr/bin/

"""

"""

import random
import json
import numpy as np
import re
import os
from collections import namedtuple
import pprint

from src.utils.loadConfig import Config
from src.utils.sqlUtils import sqlWrapper

DEBUG = False


def cleanJSON(JSONFile):
   # print("path: "+os.path.dirname(os.path.abspath(__file__)))
    dirname = os.path.dirname(os.path.abspath(__file__)) + "/"#+"simulatedData/"
    commentREGEX = re.compile(
        '/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/', re.DOTALL | re.MULTILINE)
    with open(dirname + JSONFile) as J:
        content = ''.join(J.readlines())
        match = commentREGEX.search(content)

        while match:
            content = content[:match.start()] + content[match.end():]
            match = commentREGEX.search(content)
        return json.loads(content)

conf = cleanJSON("simulConfig.json")

User = namedtuple('User', ['id', 'profile', 'cluster'])

def simulusers(params, cluster, n):
    """
    Genera usuarios simulados con un id, username y perfil

    Parameters
    ----------
    n : Int
        El numero de usuarios simulados

    Returns
    -------
    list
        Lista de usuarios con id y perfil

    """

    sqlPD = sqlWrapper(db='PD')

    users = []

    usernQuery = "SELECT username FROM users WHERE simulated = 0"

    usern = [i[0] for i in sqlPD.read(usernQuery)]
    user = [None] * n
    for i in range(n):
        user[i] = random.choice(usern)

    user_id = random.sample(range(80000), n)  # ids generados al azar

    # random.shuffle(profile)
                   # TODO: en lugar de asignarles un perfil, usar dirichlet
                   # para asignar sesiones

    readParams = "user_id,username,profile"
    sqlWrite = "INSERT INTO " \
               "users (capture_user_id,username,profile) VALUES (%s, %s, %s)"
    # sqlPD.truncateSimulated("users", readParams, sqlWrite)
    # Guardar usuarios
    sqlWrite = "INSERT INTO " \
               "users (capture_user_id,username,profile, simulated, label) " \
               "VALUES (%s, %s, %s, %s ,%s)"

    # print(len(user_id), len(user))
    for i in range(n):
        n1 = params[i][0]
        n2 = params[i][1]
        n3 = params[i][2]

        profile = [0] * int(n1 * n) + [1] * int(n2 * n) + \
            [2] * int(n3 * n)
        diff = n - len(profile)
        if diff > 0:
            for j in range(diff):
                profile.append(2)
        users.append(User(user_id[i], user[i], profile[i]))
        sqlPD.write(sqlWrite, (user_id[i], user[i], profile[i], True, cluster))

    return users


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
        La sesion a la que se agregara ruido
    p : Dict
        La tabla de probabilidades segun la que se agrega el ruido

    Returns
    -------
    list
        La sesion con ruido
    """
   # print (lista)

   # for key,values in p.items():
   #     print(key)
   #     print(values)

    l = list(lista)
    if len(lista) <= 2:
        return l

    ins = np.random.multinomial(1, p[len(lista) % 3 + 3], size=1).tolist()[
        0]  # numero de inserciones
    dele = np.random.multinomial(1, p[len(lista) % 3 + 3], size=1).tolist()[
        0]  # numero de eliminaciones

    for i in range(ins.index(1)):
        l.insert(random.randint(0, len(l)), random.choice(l))

    for i in range(dele.index(1)):
        if len(l) > 1:
            l.pop(random.randint(0, len(l) - 1))

    return l


def __probses(length, n1=70, n2=24):
    l0 = [None] * length
    l1 = [None] * length
    l2 = [None] * length

    for i in range(length):
        if i < (length * n1 / 100):
            l0[i] = random.randint(0, 10)
            l1[i] = random.randint(0, 5)
            l2[i] = random.randint(0, 2)
        elif i < (length * (n1 + n2) / 100):
            l0[i] = random.randint(0, 5)
            l1[i] = random.randint(0, 10)
            l2[i] = random.randint(0, 5)
        else:
            l0[i] = random.randint(0, 2)
            l1[i] = random.randint(0, 2)
            l2[i] = random.randint(0, 10)

    l0 = [x / sum(l0) for x in l0]
    l1 = [x / sum(l1) for x in l1]
    l2 = [x / sum(l2) for x in l2]

    return [l0, l1, l2]


def getsession():
    """
    Selecciona las sesiones desde la tabla sessions

    Returns
    -------
    list
        Lista con las sesiones segun el perfil de usuario
    """
    sqlPD = sqlWrapper(db='CD')
    # TODO: CREO que deberias leer aca el perfil y relacionarlo con el que
    # generabas randomicamente...
    sqlRead = 'SELECT sequence from sessions WHERE simulated = 0'
    rows = sqlPD.read(sqlRead)
    lr = len(rows)

    # print(n1)
    # print(n2)

    if "," in rows[0][0]:
        L = [y.split(' ') for y in [x[0] for x in rows]]
    else:
        L = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows]]
    return L


def cleanDB():
    sqlCD = sqlWrapper(db='CD')
    sqlPD = sqlWrapper(db='PD')
    deleteUsers = "DELETE FROM users WHERE simulated = 1"
    deleteSessions = "DELETE FROM sessions WHERE simulated = 1"
    deleteNodes = "DELETE FROM nodes WHERE simulated = 1"
    sqlPD.write(deleteUsers)
    sqlCD.write(deleteSessions)
    sqlCD.write(deleteNodes)
    print("Database cleaned")


def showSimulated():
    sqlCD = sqlWrapper(db='CD')
    sqlPD = sqlWrapper(db='PD')
    getUsers = "SELECT * FROM users WHERE simulated = 1 AND label = %s"
    getSessions = "SELECT * FROM sessions WHERE simulated = 1"
    getNodes = "SELECT * FROM nodes WHERE simulated = 1"
    getClusters = "SELECT DISTINCT label FROM users WHERE simulated = 1"

    print("Clusters:")
    clusters = [i[0] for i in sqlPD.read(getClusters)]
    print(clusters)

    for label in clusters:
        if (label == None):
            pass
        print("Label: " + str(label))
        print("\tUsers:")
        print([i[0] for i in sqlPD.read(getUsers % label)])
    print("Sessions:")
    print([i[0] for i in sqlCD.read(getSessions)])
    print("Nodes:")
    print([i[0] for i in sqlCD.read(getNodes)])


def dirichlet(alpha, size=200):
    """
    Genera multinomiales para un cluster
    a partir de una distribucion de dirichlet.

    Parameters
    __________
    alpha: [Int]
        Lista que representa el vector alpha de la distribucion
        de Dirichlet.
    size: Int
        Cantidad de multinomiales por generar.

    Returns
    _______
    np.Array
        Arreglo de Numpy de multinomiales generadas
    """
    dirich = np.random.dirichlet(alpha, size)
    # print(dirich[0])
    multis = []
    for u in range(size):
        multi = np.random.multinomial(n=1, pvals=dirich[u], size=1)[0]
        # print(multi)
        multis.append(multi)
    assert(len(multis) == size)
    return multis


def newGenerate():
    n_Clusters = conf["N_clusters"]
    n_usuarios = conf["N_usuarios"]
    param_dirich = conf["Param_Dirich"]

    try:
        assert(len(param_dirich) == n_Clusters)
        assert(len(param_dirich) == len(n_usuarios))
    except(AssertionError):
        print ("numero de clusters != n de parametros")
        raise ValueError

    sqlCD = sqlWrapper(db='CD')

    multis = []

    # Se generan los usuarios
    users = []
    for i in range(n_Clusters):
        parametros = dirichlet(param_dirich[i], n_usuarios[i])
        new_users = simulusers(parametros, i,  n_usuarios[i])
        multis.append(parametros)
        users += new_users

    sqlWrite = "INSERT INTO nodes (user_id, clickDate, macro_id, profile,\
                micro_id, simulated, label) VALUES " \
               "(%s,%s,%s,%s,%s,%s,%s)"
    # Se asignan las sesiones
    sessions = getsession()
    numSessions = len(sessions)
    print("numsessions: ", numSessions)

    for user in users:  # (id, perfil, label)
        userId = user.id
        profile = user.profile
        label = user.cluster
        userIdx = users.index(user) % n_usuarios[label]

        multi = multis[label][userIdx]
        idx = np.nonzero(multi == 1)[0][0] #idx = multi.index(1)
        session = sessions[idx]
        print(userIdx)
        print(multi)

        for i in range(numSessions):
            # Timestamp de inicio
            date = random.randint(1450000000, 1462534931)
            for subSession in session:
                if type(subSession) is str:
                    url = [int(x) for x in subSession.split(",")]
                    microId = url[1]
                    url = url[0]
                else:
                    url = subSession
                    microId = None
                insert = [userId, date, url, profile, microId, True, label]
                print(insert)
                sqlCD.write(sqlWrite, insert)


def generate():
    """
    DEPRECATED
    Genera los datos simulados y los guarda en la tabla simulatednodes

    Parameters
    ----------
    """
    simulationConfig = Config.getDict("simulation")
    ufrac = simulationConfig["userfrac"]
    sfrac = simulationConfig["sessionfrac"]
    numSessions = simulationConfig["sessions"]

    users = simulusers(ufrac["n1"], ufrac["n2"], ufrac[
                       "n3"], simulationConfig["users"])
    session = getsession()

    sprob = __probses(len(session), sfrac["n1"], sfrac["n2"])
    prob = __probtable(
        list({len(x) for y in session for x in y if len(x) >= 3}))

    if _DEBUG:
        pprint.pprint("dirich: " + str(dirich))
        pprint.pprint("session: " + str(session))
        pprint.pprint("sprob: " + str(sprob))
        pprint.pprint("prob: " + str(prob))

    sqlCD = sqlWrapper(db='CD')
    readParams = "user_id, clickDate, macro_id, profile, micro_id"
    sqlWrite = "INSERT INTO nodes " \
               "(user_id, clickDate, macro_id, profile, micro_id) " \
               "VALUES (%s, %s, %s, %s, %s)"
    sqlCD.truncateSimulated("nodes", readParams, sqlWrite)

    sqlWrite = "INSERT INTO nodes " \
               "(user_id, clickDate, macro_id, profile, micro_id, simulated, " \
               "label) VALUES " \
               "(%s,%s,%s,%s,%s,%s,%s)"

    for i in range(numSessions):
        for u in users:
            p = sprob[u[1]]
            idx = np.random.multinomial(1, p, size=1).tolist()[0].index(
                1)  # Se guarda su indice para poder etiquetar
            ses = session[idx]  # Se elige una sesion
            # idx = l.index(ses) + 1
            # TODO: desde aqui en adelante es lo mismo
            ses = noise(ses, prob)  # Se anade ruido
            # if u[1] == 1:  # Se corrige la etiqueta
            #     idx += len(session[0])
            # elif u[1] == 2:
            #     idx += len(session[0]) + len(session[1])
            d = random.randint(1450000000, 1462534931)  # Timestamp de inicio
            for s in ses:
                if type(s) is str:
                    url = [int(x) for x in s.split(",")]
                    L = [u[0], d, url[0], u[1], url[1], True, idx]
                else:
                    L = [u[0], d, s, u[1], None, True, idx]
                sqlCD.write(sqlWrite, L)  # Se guarda en la base de datos
                d += random.randint(1,
                                    Config.getValue('session_tlimit', 'INT') - 1)
    print ("Ok, %s users simulated, %s sessions simulated, %s nodes created" %
           (len(users), numSessions, numSessions * len(users)))

if __name__ == '__main__':
    global _DEBUG
    _DEBUG = True
    # dirichlet()
    cleanDB()
    newGenerate()
    showSimulated()
