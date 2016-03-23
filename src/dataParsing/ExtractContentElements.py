#!/usr/bin/python

"""
Extrae vectores que definen micro-estados únicos de los eventos en la base de datos.
"""

from src.utils.dataParsingUtils import *
from src.dataParsing.MicroStateVectorExtractor import *


def extractContentElements():
    """Extrae vectores de los elementos de contenido de cada estado y los almacena en la tabla respectiva.

    Returns
    -------

    """
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    msvE = MicroStateVectorExtractor()
    elementTypes = msvE.getElementTypes()
    # print('elementTypes:' +str(elementTypes))
    sqlRead = 'SELECT DISTINCT urls,contentElements from pageview'
    rows = sqlGC.read(sqlRead)
    elementsL = list()
    for i, row in enumerate(rows):
        macro_id = getMacroID(str(row[0]))
        raw = row[1]
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

    # Guarda sets únicos de elementos con sus macro_id en tabla contentElements.
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
