#!/usr/bin/python

"""
Extrae URLs únicas de los eventos en la base de datos, y los árboles completos de URLs del sitio de las capturas
"""

from src.userempathetic.utils.dataParsingUtils import hash
from src.userempathetic.utils.sqlUtils import sqlWrapper


def extractURLs():
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = 'SELECT DISTINCT url from pageview'
    rows = sqlGC.read(sqlRead)
    assert len(rows)> 0
    L = [x[0] for x in rows]  # Obtiene URLs desde los eventos capturados.

    sqlRead = 'SELECT DISTINCT urls from pageview'
    rows = sqlGC.read(sqlRead)
    assert len(rows)> 0
    URLs = [x for x in rows]
    #URLs = [json.loads(x[0]) for x in rows]  # Obtiene árboles completos de URLs del sitio en las capturas"

    # TODO: filtrar parametros de urls ?asdsa=23 .. etc.

    # for i,urltree in enumerate(URLs):
    #   print("ARBOL DE URL N°"+str(i+1)+": " + json.dumps(urltree, indent=4))

    # Función para encontrar URLs únicas dentro de un mismo árbol:

    # def getURLs(d, urlset):
    #    for k,v in d.items():
    #        urlset.add(k)
    #        if len(v) is not 0:
    #            for urlT in v:
    #                if isinstance(urlT, dict):
    #                    getURLs(urlT, urlset)
    #                else:
    #                    urlset.add(urlT.keys())
    #
    # allurls = set()
    # for urltr in URLs:
    #    getURLs(urltr,allurls)
    #
    # print("TOTAL URLs FOUND ("+str(len(allurls))+"): "+ str(allurls))

    # Limpia las tablas
    sqlPD.truncate("url")
    sqlPD.truncate("urls")

    sqlWrite = "INSERT INTO url (url) VALUES ("  # Guardar URLs desde evento.

    for url in L:
        sqlPD.write(sqlWrite + '"' + url + '");')

    sqlWrite = "INSERT INTO urls (id, urls) VALUES (%s,%s)"  # Guardar Árboles completos de URLs.

    for urlstree in URLs:
        #urljsonstr = json.dumps(urlstree).replace(' ', '')
        urljsonstr = urlstree[0].replace(' ', '')
        # print(urljsonstr)
        sqlPD.write(sqlWrite, (hash(urljsonstr), urljsonstr))

if __name__ == '__main__':
    extractURLs()
