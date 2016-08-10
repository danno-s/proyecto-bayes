# -*- coding: utf-8 -*-

"""
Modulo para lectura y escritura en bases de datos SQL, mediante la libreria mysql.connector
"""

import os
import json
import pymysql
class sqlWrapper:
    """
    Clase genera wrappers para la conexion a bases de datos SQL
    """
    conns = dict()  # Diccionario donde se encuentran los datos de conexion a las bases de datos

    def __init__(self, db):
        """Constructor de la clase

        Parameters
        ----------
        db : str
            Abreviatura de la base de datos a la que se desea acceder

        Returns
        -------
        sqlWrapper
            El wrapper creado
        """
        if db.upper() in ['GC', 'PD', 'GT', 'CD', 'FT', 'CL']:
            self.db = db
        else:
            raise Exception
        if len(self.conns) == 0:
            # try:
            self.__loadConnections()
            # except:
            # raise ConnectionError #TODO: Definir excepciones de este estilo

    def setDB(self, db):
        """Define la base de datos a la que se conectara

        Parameters
        ----------
        db : str
            Abreviatura de la base de datos a la que se desea acceder
        """
        self.db = db

    def truncate(self, table, where_condition=None):
        """Trunca la tabla indicada

        Parameters
        ----------
        table : str
            El nombre de la tabla a truncar
        where_condition : str
            Si existe, se realiza un 'DELETE FROM table WHERE where_condition'
        """
        cnx = pymysql.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'],
                                      host=self.conns[self.db]['host'], database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        if where_condition:
            cursor.execute('DELETE FROM ' + table +
                           " WHERE " + where_condition)
        else:
            cursor.execute('TRUNCATE ' + table)

        cnx.commit()
        cnx.close()

    def truncateSimulated(self, table, readParams, sqlWrite):
        old_rows = self.read("SELECT " + readParams +
                             " FROM " + table + " WHERE simulated = 0")
        self.truncate(table)
        for row in old_rows:
            self.write(sqlWrite, row)

    def read(self, sqlRead):
        """Efectua la consulta sqlRead

        Parameters
        ----------
        sqlRead : str
            La consulta que se hara a la base de datos del sqlWrapper.

        Returns
        -------
        List
            La tabla de los resultados de la consulta, en forma de lista de tuplas.
        """
        cnx = pymysql.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'],
                                      host=self.conns[self.db]['host'], database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        cursor.execute(sqlRead)
        rows = cursor.fetchall()
        cnx.close()
        return rows

    def write(self, sqlWrite, item=None):
        """Efectua la escritura sqlWrite.

        Notes
            Se pueden incluir los valores dentro del atributo sqlWrite o ser pasados a traves de item. En cuyo caso,
        el query debe contener los caracteres %s indicando cuantos valores son pasados.

        Parameters
        ----------
        sqlWrite : str
            La escritura a realizar
        item : List
            Los item a guardar en la base de datos

        Returns
        -------

        """
        cnx = pymysql.connect(user=self.conns[self.db]['user'], password=self.conns[self.db]['passwd'],
                                      host=self.conns[self.db]['host'], database=self.conns[self.db]['db'])
        cursor = cnx.cursor()
        if item is not None:
            try:
                cursor.execute(sqlWrite, item)
            except:
                print(item)
                raise
        else:
            cursor.execute(sqlWrite)
        cnx.commit()
        cnx.close()

    def __loadConnections(self):
        """Carga archivo de conexiones con datos de acceso a cada base de datos y las asocia a las abreviaturas definidas.
        Returns
        -------

        """
        with open(os.path.dirname(os.path.dirname(__file__)) + '/connections.json', 'r') as f:
            connectionsJSON = f.read()
        connections = json.loads(connectionsJSON)
        try:
            self.conns['GC'] = connections['guidecapture']
            self.conns['PD'] = connections['parsedData']
            self.conns['CD'] = connections['coreData']
            self.conns['GT'] = connections['groundTruth']
            self.conns['FT'] = connections['features']
            self.conns['CL'] = connections['clusters']
        except:
            raise
