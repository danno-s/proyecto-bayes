#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extrae vectores que definen micro-estados unicos de los eventos en la base de datos.
"""

from src.utils.dataParsingUtils import *
from src.dataParsing.MicroStateVectorExtractor import *
import src.utils as utils
capture_table = utils.loadConfig.Config.getValue("capture_table")


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

    msvE = MicroStateVectorExtractor()
    elementTypes = msvE.getElementTypes()
    # print('elementTypes:' +str(elementTypes))
    sqlRead = 'SELECT DISTINCT url,urls,contentElements from ' + capture_table
    rows = sqlGC.read(sqlRead)
    elementsL = list()
    for i, row in enumerate(rows):
        macro_id = getMacroID(row[0],row[1])
        raw = row[2]
        contentElementUnique = json.loads(raw)
        eL = (macro_id,)
        try:
            data = msvE.getStateVectors(contentElementUnique)
        except:
            print("Error en fila: " + str(i))
            print(json.dumps(contentElementUnique, indent=2))
            raise
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
    for tp in uniqueElementsS:
        sqlPD.write(sqlWrite, tp)


if __name__ == '__main__':
    extractContentElements()
