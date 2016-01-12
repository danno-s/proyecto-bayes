#!/usr/bin/python

import json
import mysql.connector
import hashlib
import os


with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
	connectionsJSON = f.read()

def hash(string):
    return hashlib.md5(string.encode()).hexdigest()

connections = json.loads(connectionsJSON)

connRead = connections[0]
connWrite = connections[1]

sqlRead = 'SELECT DISTINCT url from pageview'
cnx = mysql.connector.connect(user=connRead['user'], password=connRead['passwd'], host=connRead['host'],database=connRead['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
rows = cursor.fetchall()

L = [x[0] for x in rows] # Obtiene URLs desde los eventos capturados.

sqlRead = 'SELECT DISTINCT urls from pageview'
cursor.execute(sqlRead)
rows = cursor.fetchall()

URLs = [json.loads(x[0]) for x in rows]    # Obtiene árboles completos de URLs del sitio en las capturas"

cnx.close()

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


cnx = mysql.connector.connect(user=connWrite['user'], password=connWrite['passwd'], host=connWrite['host'],database=connWrite['db'])
cursor = cnx.cursor()

## RESETEAR TABLAS:
cursor.execute("TRUNCATE url")
cursor.execute("TRUNCATE urls")

# Guardar URLs desde evento.

sqlWrite = "INSERT INTO url (url) VALUES ("

for url in L:
    cursor.execute(sqlWrite + '"' + url + '");')
cnx.commit()


# Guardar Árboles completos de URLs.

sqlWrite = "INSERT INTO urls (id, urls) VALUES (%s,%s)"

for urlstree in URLs:
    urljsonstr = json.dumps(urlstree).replace('\"','\\"')
    cursor.execute(sqlWrite,(hash(urljsonstr) , urljsonstr))

cnx.commit()
cnx.close()
