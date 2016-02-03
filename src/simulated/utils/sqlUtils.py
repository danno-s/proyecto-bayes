"""
Clase genera wrappers para la conexión a bases de datos
"""

import os
import json
import mysql.connector


class sqlWrapper:
    """ Diccionario donde se encuentran los datos de conexión a las bases de datos """
    conns = dict()

    def __init__(self,db):
        """
        Constructor de la clase

        Parameters
        ----------
        db : string
            La base de datos a la que se conectara

        Returns
        -------
        sqlWrapper
            El wrapper creado
        """
        if db.upper() in ['GC', 'PD', 'GT','CD','FT']:
            self.db = db
        else:
            raise Exception
        if len(self.conns) == 0:
            # try:
            self.__loadConnections()
            # except:
            #    raise ConnectionError

    def setDB(self,db):
        """
        Define la base de datos a la que se conectara

        Parameters
        ----------
        db : string
            El nombre de la base de datos a conectar
        """
        self.db = db

    def truncate(self,table):
        """
        Trunca la tabla indicada

        Parameters
        ----------
        table : string
            El nombre de la tabla a truncar
        """
        cnx = mysql.connector.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'], host=self.conns[self.db]['host'],database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        cursor.execute('TRUNCATE '+table)
        cnx.commit()
        cnx.close()

    def read(self,sqlRead):
        """
        Efectúa la consulta sqlRead

        Parameters
        ----------
        sqlRead : string
            La consulta que se hará

        Returns
        -------
        List
            La tabla de los resultados de la consulta, en forma de lista
        """
        cnx = mysql.connector.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'], host=self.conns[self.db]['host'],database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        cursor.execute(sqlRead)
        rows = cursor.fetchall()
        cnx.close()
        return rows

    def write(self,sqlWrite,item = None):
        """
        Efectúa la escritura sqlWrite

        Parameters
        ----------
        sqlWrite : string
            La escritura a realizar
        item : List
            Los item a guardar en la base de datos

        Returns
        -------

        """
        cnx = mysql.connector.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'], host=self.conns[self.db]['host'],database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        if item is not None:
            try:
                cursor.execute(sqlWrite,item)
            except:
                print(item)
                raise
        else:
            cursor.execute(sqlWrite)
        cnx.commit()
        cnx.close()

    def __loadConnections(self):
        with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
            connectionsJSON = f.read()
        connections = json.loads(connectionsJSON)
        try:
            self.conns['GC'] = connections['guidecapture']
            self.conns['PD'] = connections['parsedData']
            self.conns['CD'] = connections['coreData']
            # self.conns['GT'] = connections['groundTruth']
            # self.conns['FT'] = connections['features']


        except:
            raise
