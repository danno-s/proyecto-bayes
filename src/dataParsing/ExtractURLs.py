# -*- coding: utf-8 -*-

from src.utils.sqlUtils import sqlWrapper


def extractURLs():
    """Extrae URLs unicas de los datos capturados en la base de datos, y los arboles completos de URLs del
    sitio de las capturas.

    Returns
    -------

    """
    try:
        # Asigna las bases de datos que se accederan
        sqlGC = sqlWrapper(db='GC')
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = 'SELECT DISTINCT url from pageview2'
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    L = [x[0] for x in rows]  # Obtiene URLs desde los eventos capturados.

    sqlRead = 'SELECT DISTINCT urls from pageview2'
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    URLs = [x for x in rows]
    # URLs = [json.loads(x[0]) for x in rows]  # Obtiene arboles completos de
    # URLs del sitio en las capturas"

    # TODO: filtrar parametros de urls ?asdsa=23 .. etc.

    # Limpia las tablas
    sqlPD.truncate("url")
    sqlPD.truncate("urls")

    sqlWrite = "INSERT INTO url (url) VALUES ("  # Guardar URLs desde evento.
    i=0
    for url in L:
        print(i)
        i+=1
        sqlPD.write(sqlWrite + '"' + url + '");')

    # Guardar arboles completos de URLs.
    sqlWrite = "INSERT INTO urls (urls) VALUES ("

    for urlstree in URLs:
        # urljsonstr = json.dumps(urlstree).replace(' ', '')
        urljsonstr = urlstree[0].replace(' ', '')
        # print(urljsonstr)
        sqlPD.write(sqlWrite + "'" + urljsonstr + "');")


if __name__ == '__main__':
    extractURLs()
