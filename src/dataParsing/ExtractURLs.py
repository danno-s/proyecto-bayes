#!/usr/bin/python
from src.utils.sqlUtils import sqlWrapper


def extractURLs():
    """Extrae URLs únicas de los datos capturados en la base de datos, y los árboles completos de URLs del
    sitio de las capturas.

    Returns
    -------

    """
    try:
        sqlGC = sqlWrapper(db='GC')  # Asigna las bases de datos que se accederán
        sqlPD = sqlWrapper(db='PD')
    except:
        raise
    sqlRead = 'SELECT DISTINCT url from pageview'
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    L = [x[0] for x in rows]  # Obtiene URLs desde los eventos capturados.

    sqlRead = 'SELECT DISTINCT urls from pageview'
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    URLs = [x for x in rows]
    # URLs = [json.loads(x[0]) for x in rows]  # Obtiene árboles completos de URLs del sitio en las capturas"

    # TODO: filtrar parametros de urls ?asdsa=23 .. etc.

    # Limpia las tablas
    sqlPD.truncate("url")
    sqlPD.truncate("urls")

    sqlWrite = "INSERT INTO url (url) VALUES ("  # Guardar URLs desde evento.

    for url in L:
        sqlPD.write(sqlWrite + '"' + url + '");')

    sqlWrite = "INSERT INTO urls (urls) VALUES ("  # Guardar Árboles completos de URLs.

    for urlstree in URLs:
        # urljsonstr = json.dumps(urlstree).replace(' ', '')
        urljsonstr = urlstree[0].replace(' ', '')
        # print(urljsonstr)
        sqlPD.write(sqlWrite + "'" + urljsonstr + "');")


if __name__ == '__main__':
    extractURLs()
