#!/usr/bin/python

"""
Extrae vectores que definen micro-estados únicos de los eventos en la base de datos.
"""

from src.utils.dataParsingUtils import *
from src.dataParsing.MicroStateVectorExtractor import *


def extractContentElements():
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise

    msvE = MicroStateVectorExtractor()
    elementTypes = msvE.getElementTypes()
    print('elementTypes:' +str(elementTypes))
    sqlRead = 'SELECT DISTINCT urls,contentElements from pageview'
    rows = sqlGC.read(sqlRead)
    allElementsL = list()
    for i,row in enumerate(rows):
        eL = tuple()
        data = dict()
        macro_id = getMacroID(str(row[0]))
        raw = row[1]
        contentElementUnique = json.loads(raw)
        eL=eL+(macro_id,)
        try:
            data = msvE.getStateVectors(contentElementUnique)
        except:
            print("Error en fila: "+  str(i))
            print(json.dumps(contentElementUnique,indent=2))
            raise
        for type in elementTypes:
            eL = eL+(data[type],)
        eL = eL+(raw,)
        allElementsL.append(eL)

    macro_ids = set([x[0] for x in allElementsL])

    macroD = dict()
    for id in macro_ids:
        micro_states = set()
        for x in allElementsL:
            if x[0] == id:
                element_states = tuple()
                for st in x[1:]:
                    element_states += (st,)
                micro_states.add(element_states)
        macroD[id]=micro_states

    for id,values in macroD.items():
        print("MacroID "+str(id)+" :\n")
        for l in values:
            tp = (id,)
            for x in l[:-1]:
                tp += (x,)
            print("\t"+str(tp))

    print("Total different micro states:" + str(sum([len(x) for x in macroD.values()])))


    # Limpia las tablas

    sqlPD.truncate("contentElements")

    # Guarda sets únicos de elementos con sus macro_id en tabla contentElements.

    # Primero se guarda el marco_id y la estructura json raw
    sqlWrite = "INSERT INTO contentElements (macro_id,raw) VALUES (%s,%s)"
    for id,values in macroD.items():
        for l in values:
            tp = (id,l[-1])
            sqlPD.write(sqlWrite,tp)
            # Luego se realiza un update sobre esta fila insertada
            # OBS: Se hizo así debido a que mysql.connector no soporta insertar más de 5 valores simultáneamente.
            sqlUpdate = "UPDATE contentElements SET "
            for type in elementTypes:
                sqlUpdate += type+'=%s,'
            tp = tuple()
            for x in l[:-1]:
                tp += (x,)
            sqlUpdate = sqlUpdate[:-1] + " ORDER BY id DESC LIMIT 1"
            sqlPD.write(sqlUpdate,tp)



if __name__ == '__main__':
    extractContentElements()
