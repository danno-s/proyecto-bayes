#!/usr/bin/

"""

"""

import random
import numpy as np
from src.simulated.utils.sqlUtils import sqlWrapper

def simulusers():
    n = 200

    usern = ["U8213221", "U6355477", "jefe_local"]
    user = [None]*n
    for i in range(n):
        user[i] = random.choice(usern)

    id = random.sample(range(2000), n)
    perfil = [0]*int(0.70*n)+[1]*int(0.23*n)+[2]*int(0.07*n)
    random.shuffle(perfil)

    sqlPD = sqlWrapper(db='PD')
    sqlPD.truncate("users")  # Limpia la tabla
    sqlWrite = "INSERT INTO users (id_usuario,username,perfil) VALUES (%s, %s, %s)" # Guardar usuarios

    for i in range(len(id)):
        sqlPD.write(sqlWrite,(id[i],user[i],perfil[i]))

    return list(zip(id,perfil))

def __vect(n):
    v = [0]*int(n/2)
    for i in range(len(v)):
        v[i] = 0.5**(i+1)
    r = 1.0 - sum(v)
    if 1.0 > r:
        v[0] += r
    return tuple(v)

def __probtable(list):
    lp = [0] * len(list)
    for i in range(len(list)):
        p = __vect(list[i])
        if not p:
            p = [0]
        lp[i] = p

    return dict(zip(list,lp))

def noise(lista,p):
    l = list(lista)
    if len(lista) <= 2:
        return l
        # r = random.randint(0,1)
        # if r==1:
        #     l.insert(random.randint(0,len(l)),random.choice(l))
        # r = random.randint(0,1)
        # if r == 1 and 1 < len(l):
        #     l.pop(random.randint(0,len(l)-1))

    ins = np.random.multinomial(1, p[len(lista)], size=1).tolist()[0]
    dele = np.random.multinomial(1, p[len(lista)], size=1).tolist()[0]

    for i in range(ins.index(1)):
        l.insert(random.randint(0,len(l)),random.choice(l))

    for i in range(dele.index(1)):
        if len(l)>1:
            l.pop(random.randint(0,len(l)-1))

    return l

def getsession():
    sqlPD = sqlWrapper(db='CD')
    sqlRead = 'SELECT sequence from sessions'
    rows = sqlPD.read(sqlRead)
    lr = len(rows)

    L = [None]*3

    if "," in rows[0]:
        L[0] = [y.split(' ') for y in [x[0] for x in rows[:int(lr*0.7)]]]
        L[1] = [y.split(' ') for y in [x[0] for x in rows[int(lr*0.7):int(lr*0.94)]]]
        L[2] = [y.split(' ') for y in [x[0] for x in rows[int(lr*0.94):]]]
    else:
        L[0] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[:int(lr*0.7)]]]
        L[1] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[int(lr*0.7):int(lr*0.94)]]]
        L[2] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[int(lr*0.94):]]]

    return L

def generate(n):
    users = simulusers()
    session = getsession()
    prob = __probtable(list({len(x) for y in session for x in y if len(x) >= 3}))

    sqlCD = sqlWrapper(db='CD')
    sqlCD.truncate("simulatednodes")
    sqlWrite = "INSERT INTO simulatednodes (user_id, clickDate, urls_id,profile,micro_id) VALUES (%s,%s,%s,%s,%s)"

    for i in range(n):
        for u in users:
            l = session[u[1]]
            ses = random.choice(l)
            ses = noise(ses,prob)
            d = random.randint(1450000000,1462534931)
            for s in ses:
                if type(s) is str:
                    url = [int(x) for x in s.split(",")]
                    L= [u[0],d,url[0],u[1],url[1]]
                else:
                    L = [u[0],d,s,u[1],None]
                sqlCD.write(sqlWrite, L)
                d += random.randint(1,59)


if __name__ == '__main__':
    generate(1)