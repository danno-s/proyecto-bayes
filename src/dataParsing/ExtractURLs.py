# -*- coding: utf-8 -*-

from src.utils.sqlUtils import sqlWrapper
from src.utils.loadConfig import Config

capture_table = Config.getValue("capture_table")

def extractURLs():
    """Extrae macro_ids unicas de los datos capturados en la base de datos, y los arboles completos de macro_ids del
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
    sqlRead = 'SELECT DISTINCT url from ' + capture_table
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    L = []
    for x in rows:  # Obtiene macro_ids desde los eventos capturados.
        urlstr = x[0]
        if urlstr.endswith(' undefined'):
            urlstr = urlstr[:-10]
        L.append(urlstr)

    sqlRead = 'SELECT DISTINCT urls from ' + capture_table
    rows = sqlGC.read(sqlRead)
    assert len(rows) > 0
    URLs = [x for x in rows]

    # Limpia las tablas
    sqlPD.truncate("url")
    sqlPD.truncate("urls")

    sqlWrite = "INSERT INTO url (url) VALUES ("  # Guardar macro_ids desde evento.
    i=0
    print(str(len(L))+ " url encontradas.")
    for url in L:
        i+=1
        sqlPD.write(sqlWrite + '"' + url + '");')

    # Guardar arboles completos de macro_ids.
    sqlWrite = "INSERT INTO urls (urls) VALUES ("

    print(str(len(URLs))+ " arboles de URLs encontrados.")

    for urlstree in URLs:
        urljsonstr = urlstree[0].replace(' ', '')
        sqlPD.write(sqlWrite + "'" + urljsonstr + "');")


if __name__ == '__main__':
    extractURLs()
