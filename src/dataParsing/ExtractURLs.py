#!/usr/bin/python

import json
import hashlib
from src.sqlUtils.sqlUtils import sqlWrapper

def hash(string):
    return hashlib.md5(string.encode()).hexdigest()

sqlGC = sqlWrapper(db='GC')
sqlPD = sqlWrapper(db='PD')

sqlRead = 'SELECT DISTINCT url from pageview'
rows = sqlGC.read(sqlRead)

L = [x[0] for x in rows] # Obtiene URLs desde los eventos capturados.

sqlRead = 'SELECT DISTINCT urls from pageview'
rows = sqlGC.read(sqlRead)

URLs = [json.loads(x[0]) for x in rows]    # Obtiene árboles completos de URLs del sitio en las capturas"

# TODO: filtrar parametros de urls ?asdsa=23 .. etc.

#for i,urltree in enumerate(URLs):
#   print("ARBOL DE URL N°"+str(i+1)+": " + json.dumps(urltree, indent=4))

# Función para encontrar URLs únicas dentro de un mismo árbol:

#def getURLs(d, urlset):
#    for k,v in d.items():
#        urlset.add(k)
#        if len(v) is not 0:
#            for urlT in v:
#                if isinstance(urlT, dict):
#                    getURLs(urlT, urlset)
#                else:
#                    urlset.add(urlT.keys())
#
#allurls = set()
#for urltr in URLs:
#    getURLs(urltr,allurls)
#
#print("TOTAL URLs FOUND ("+str(len(allurls))+"): "+ str(allurls))


## RESETEAR TABLAS:
sqlPD.truncate("url")
sqlPD.truncate("urls")

# Guardar URLs desde evento.

sqlWrite = "INSERT INTO url (url) VALUES ("

for url in L:
    sqlPD.write(sqlWrite + '"' + url + '");')

# Guardar Árboles completos de URLs.

sqlWrite = "INSERT INTO urls (id, urls) VALUES (%s,%s)"

for urlstree in URLs:
    urljsonstr = json.dumps(urlstree).replace(' ', '')
    print(urljsonstr)
    sqlPD.write(sqlWrite,(hash(urljsonstr), urljsonstr))
