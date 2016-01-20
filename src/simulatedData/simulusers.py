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

    id = random.sample(range(2000), n)
    perfil = [0]*int(0.70*n)+[1]*int(0.24*n)+[2]*int(0.06*n)
    random.shuffle(perfil)

    return list(zip(id,user,perfil))

def geturls():
    sqlPD = sqlWrapper(db='PD')
    sqlRead = 'SELECT id from urls'
    rows = sqlPD.read(sqlRead)

    return [x[0] for x in rows]

def noise(list,n):
    l = list
    for i in range(n):
        r = random.randint(0,1)
        if r==0:
            l.insert(random.randint(0,len(l)),random.randint(0,30))
        else:
            if len(l)>1:
                l.pop(random.randint(0,len(l)-1))
    return l

def getsession():
    sqlPD = sqlWrapper(db='PD')
    sqlRead = 'SELECT urls from sessiondata'
    rows = sqlPD.read(sqlRead)

    L = [None]*3
    L[0] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[:21]]]
    L[1] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[21:28]]]
    L[2] = [[int(s) for s in y.split(' ')] for y in [x[0] for x in rows[28:]]]

    return L

def generate(n):
    users = simulusers()
    urls = geturls()
    session = getsession()

    sqlPD = sqlWrapper(db='PD')
    sqlPD.truncate("simulated")
    sqlWrite = "INSERT INTO simulated (id_urltree, hash_urltree, clickdate,id_user,username,perfil) VALUES (%s,%s,%s,%s,%s,%s)"

    for i in range(n):
        for u in users:
            l = session[u[2]]
            ses = random.choice(l)
            ses = noise(ses,3)
            d = random.randint(1450000000,1452534931)
            for s in ses:
                try:
                    url = urls[s-1]
                except IndexError:
                    print(len(url))
                    print(s)
                    print(ses)
                    exit()
                L= [s-1,url,d]
                L.extend(u)
                sqlPD.write(sqlWrite, L)
                d += random.randint(1,49)


if __name__ == '__main__':
    generate(5)

