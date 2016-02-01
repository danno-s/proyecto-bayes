#!/usr/bin/

"""

"""

import random
import numpy as np
from src.utils.sqlUtils import sqlWrapper

def simulusers():
    n = 200

    id = random.sample(range(2000), n)
    perfil = [0]*int(0.70*n)+[1]*int(0.23*n)+[2]*int(0.07*n)
    random.shuffle(perfil)

    return list(zip(id,perfil))

def geturls():
    sqlPD = sqlWrapper(db='PD')
    sqlRead = 'SELECT id from urls'
    rows = sqlPD.read(sqlRead)

    return [x[0] for x in rows]

def getmicro():
    sqlPD = sqlWrapper(db='PD')
    sqlRead = 'SELECT id from contentElements'
    rows = sqlPD.read(sqlRead)

    return [x[0] for x in rows]

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

def noise(list,p):
    l = list
    if len(list) <= 2:
        return l
        # r = random.randint(0,1)
        # if r==1:
        #     l.insert(random.randint(0,len(l)),random.choice(l))
        # r = random.randint(0,1)
        # if r == 1 and 1 < len(l):
        #     l.pop(random.randint(0,len(l)-1))

    ins = np.random.multinomial(1, p[len(list)], size=1).tolist()[0]
    dele = np.random.multinomial(1, p[len(list)], size=1).tolist()[0]

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
    L[0] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[:int(lr*0.7)]]]
    L[1] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[int(lr*0.7):int(lr*0.94)]]]
    L[2] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[int(lr*0.94):]]]

    return L

# def setsession():
#     a = open("sesiones.txt","w")
#
#     L = [None]*3
#     L[0] = [np.random.choice(range(1,15),random.randint(1,20)).tolist() for x in range(5)]
#     a.write(str(L[0])+ "\n")
#     L[1] = [np.random.choice(range(15,25),random.randint(1,20)).tolist() for x in range(5,9)]
#     a.write(str(L[1])+ "\n")
#     L[2] = [np.random.choice(range(25,31),random.randint(1,20)).tolist() for x in range(9,12)]
#     a.write(str(L[2])+ "\n")
#
#     a.close()
#
#     return L

def generate(n):
    users = simulusers()
    urls = geturls()
    micro = getmicro()
    session = getsession()
    prob = __probtable(list({len(x) for y in session for x in y if len(x) >= 3}))

    sqlPD = sqlWrapper(db='CD')
    sqlPD.truncate("simulated")
    sqlWrite = "INSERT INTO simulatednodes (user_id, clickDate, urls_id,profile,micro_id) VALUES (%s,%s,%s,%s,%s)"

    for i in range(n):
        for u in users:
            m = random.choice(micro)
            l = session[u[1]]
            ses = random.choice(l)
            ses = noise(ses,prob)
            d = random.randint(1450000000,1462534931)
            for s in ses:
                if s==-1:
                    print(ses)
                try:
                    url = urls[s-1]
                except IndexError:
                    print(len(url))
                    print(s)
                    print(ses)
                    exit()
                L= [u[0],d,s,u[1],m]
                L.extend(u)
                sqlPD.write(sqlWrite, L)
                d += random.randint(1,59)


if __name__ == '__main__':
    generate(1)