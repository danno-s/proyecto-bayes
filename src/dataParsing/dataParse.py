#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from src.utils.dataParsingUtils import *


def __query(n):
    return "SELECT urls, variables, clickDate, contentElements FROM pageview LIMIT " + str(n) + ", 1"


def dataParse():
    """Extrae datos desde pageview y los guarda en nodes en un formato adecuado

    Returns
    -------

    """
    sqlGC = sqlWrapper(db='GC')
    sqlCD = sqlWrapper(db='CD')

    sqlCD.truncate("nodes")

    sqlWrite = "INSERT INTO nodes (user_id, clickDate, urls_id, profile, micro_id) VALUES (%s,%s,%s,%s,%s)"
    i = 0

    while True:
        info = sqlGC.read(__query(i))
        if not info:
            break
        url = getMacroID(info[0][0])
        micro = getMicroID(info[0][3])
        usr = int(json.loads(info[0][1])['id_usuario'])
        profile = json.loads(info[0][1])['profile']
        click = info[0][2]

        sqlCD.write(sqlWrite, (usr, click, url, profile, micro))

        i += 1

    print("Total nodes: " + str(i))


if __name__ == '__main__':
    dataParse()
