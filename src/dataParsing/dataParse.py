#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from src.utils.dataParsingUtils import *

from src.utils.sqlUtils import sqlWrapper


def __query(n):
    from src.utils.loadConfig import Config
    capture_table = Config.getValue("capture_table")

    return "SELECT id, url, urls, variables, clickDate, contentElements FROM "+ capture_table +" WHERE variables NOT LIKE 'null'"+" LIMIT " + str(n) + ", 1"


def dataParse():
    """Extrae datos desde capture_table y los guarda en nodes en un formato adecuado

    Returns
    -------

    """
    sqlGC = sqlWrapper(db='GC')
    sqlCD = sqlWrapper(db='CD')

    sqlCD.truncate("nodes")

    sqlWrite = "INSERT INTO nodes (user_id, clickDate, macro_id, profile, micro_id) VALUES (%s,%s,%s,%s,%s)"
    i = 0
    Nnodes= 0
    while True:
        info = sqlGC.read(__query(i))
        if not info:
            break
        row = info[0]
        urlstr = row[1]
        macro = getMacroID((urlstr,row[2],row[3]))
        micro = getMicroID(row[5])
        if not macro:
            i+=1
            continue
        if not micro:
            micro = -1
        usr = getUserID(row[3])
        if not usr:
            i+=1
            continue
        profile = json.loads(row[3])['profile']
        if not profile:
            profile = None
        click = row[4]
        sqlCD.write(sqlWrite, (usr, click, macro, profile, micro))
        i += 1
        Nnodes += 1

    print("Total nodes: " + str(Nnodes))


if __name__ == '__main__':
    dataParse()
