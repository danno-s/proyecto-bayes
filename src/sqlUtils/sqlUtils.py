#!/usr/bin/python

import os
import json
import mysql.connector


class sqlWrapper:
    conns = dict()

    def __init__(self,db):
        self.db = db
        if len(self.conns) == 0:
            self.loadConnections()

    def loadConnections(self):
        with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
            connectionsJSON = f.read()
        connections = json.loads(connectionsJSON)
        self.conns['GC'] = connections[0]
        self.conns['PD'] = connections[1]

    def setDB(self,db):
        self.db = db

    def truncate(self,table):
        cnx = mysql.connector.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'], host=self.conns[self.db]['host'],database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        cursor.execute('TRUNCATE '+table)
        cnx.commit()
        cnx.close()

    def read(self,sqlRead):
        cnx = mysql.connector.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'], host=self.conns[self.db]['host'],database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        cursor.execute(sqlRead)
        rows = cursor.fetchall()
        cnx.close()
        return rows

    def write(self,sqlWrite,item = None):
        cnx = mysql.connector.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'], host=self.conns[self.db]['host'],database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        if item != None:
            cursor.execute(sqlWrite,item)
        else:
            cursor.execute(sqlWrite)
        cnx.commit()
        cnx.close()
