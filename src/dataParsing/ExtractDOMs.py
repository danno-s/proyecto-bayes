#!/usr/bin/python

import json
import mysql.connector
from htmldom import htmldom
from htmltreediff import diff
with open('connections.json', 'r') as f:
	connectionsJSON = f.read()
	
connections = json.loads(connectionsJSON)

connRead = connections[0]
connWrite = connections[1]

#print(connRead)
#print(connWrite)

sqlRead = 'select html from pageview'
cnx = mysql.connector.connect(user=connRead['user'], password=connRead['passwd'], host=connRead['host'],database=connRead['db'])
cursor = cnx.cursor()

cursor.execute(sqlRead)
cnx.close()

rows = cursor.fetchall()
L = list()
for row in rows:
	 L.append(row[0])
html1 = L[len(L)-2]
html2= L[len(L)-1]
#print(html)
DOM1 = htmldom.HtmlDom().createDom(html1)
DOM2 = htmldom.HtmlDom().createDom(html2)
h1 = DOM1.find("*");
h2 = DOM2.find("*");

import difflib

html_1 = """
<p>a</p>
    <td>b</td>
"""
html_2 = """
<h2>a</h2>
    <td>b</td>
"""

diff_html = ""
theDiffs = difflib.ndiff(h1.html().splitlines(), h2.html().splitlines())
for eachDiff in theDiffs:
    if (eachDiff[0] == "-"):
        diff_html += "<del>%s</del>\n" % eachDiff[1:].strip()
    elif (eachDiff[0] == "+"):
        diff_html += "<ins>%s</ins>\n" % eachDiff[1:].strip()

print(diff_html)