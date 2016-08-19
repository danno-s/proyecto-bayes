#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from src.utils.dataParsingUtils import *
import src.utils as utils
capture_table = utils.loadConfig.Config.getValue("capture_table")

def __query(n):
    return "SELECT url, urls, variables, clickDate, contentElements FROM "+ capture_table +" LIMIT " + str(n) + ", 1"


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

    while True:
        info = sqlGC.read(__query(i))
        if not info:
            break
        macro = getMacroID(info[0][0],info[0][1])
        micro = getMicroID(info[0][4])
        usr = getUserID(json.loads(info[0][2])['id_usuario'])
        profile = json.loads(info[0][2])['profile']
        click = info[0][3]

        sqlCD.write(sqlWrite, (usr, click, macro, profile, micro))

        i += 1

    print("Total nodes: " + str(i))


if __name__ == '__main__':
    dataParse()
