#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extrae vectores que definen micro-estados unicos de los eventos en la base de datos.
"""

from src.utils.dataParsingUtils import *
from src.dataParsing.MicroStateVectorExtractor import *
from src.dataParsing.DataParser import DataParser


def extractContentElements():
    """Extrae vectores de los elementos de contenido de cada estado y los almacena en la tabla respectiva.

    Returns
    -------

    """
    try:
        # Asigna las bases de datos que se accederan
        sqlGC = sqlWrapper(db='GC')
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    dp = DataParser()
    msvE = MicroStateVectorExtractor()
    elementTypes = msvE.getElementTypes()
    # print('elementTypes:' +str(elementTypes))
    from src.utils.loadConfig import Config
    capture_table = Config.getValue("capture_table")

    sqlRead = 'SELECT DISTINCT url,urls,variables, contentElements from ' + capture_table + " WHERE variables NOT LIKE 'null'"
    rows = sqlGC.read(sqlRead)
    elementsL = list()
    for i, row in enumerate(rows):
        macro_id = dp.getMacroID((row[0], row[1], row[2]))
        raw = row[3]
        contentElementUnique = json.loads(raw)
        eL = (macro_id,)
        try:
            data = msvE.getStateVectors(contentElementUnique)
        except:
            print("Error en fila: " + str(i))
            print(json.dumps(contentElementUnique, indent=2))
            raise
        #if allElementsEmpty(data):
        #    continue
        for el_type in elementTypes:
            eL = eL + (data[el_type],)
        eL = eL + (raw,)
        elementsL.append(eL)
    uniqueElementsS = list(sorted(set(elementsL), key=lambda s: int(s[0])))

    #    for tp in uniqueElementsS:
    #       print(str(tp))

    print("Total different micro states:" + str(len(uniqueElementsS)))

    # Limpia las tablas

    sqlPD.truncate("contentElements")

    # Guarda sets unicos de elementos con sus macro_id en tabla
    # contentElements.
    sqlWrite = "INSERT INTO contentElements (macro_id"
    for el in elementTypes:
        sqlWrite += ',' + el
    sqlWrite += ",raw) VALUES (%s"
    for el in elementTypes:
        sqlWrite += ",%s"
    sqlWrite += ",%s)"
    #    print(sqlWrite)
    sqlPD.writeMany(sqlWrite, uniqueElementsS)


def allElementsEmpty(data):
    for v in data.values():
        if v is not '':
            return False
    return True


if __name__ == '__main__':
    extractContentElements()
