# -*- coding: utf-8 -*-

"""
Modulo para cargar configuracion desde un archivo "config.json" en el path del proyecto.
"""

import json
import os
import jsmin
from src.clustering.clusterings.userclusterings.UserURLsBelongingClustering import UserURLsBelongingClustering
from src.clustering.clusterings.userclusterings.UserLRSHistogramClustering import UserLRSHistogramClustering
from src.clustering.clusterings.userclusterings.FullUserClustering import FullUserClustering

from src.clustering.clusterings.sessionclusterings.SessionUserClustersBelongingClustering import SessionUserClustersBelongingClustering
from src.clustering.clusterings.sessionclusterings.SessionLRSBelongingClustering import SessionLRSBelongingClustering
from src.clustering.clusterings.sessionclusterings.DirectSessionClustering import DirectSessionClustering
from src.clustering.clusterings.sessionclusterings.FullSessionClustering import FullSessionClustering
from src.clustering.clusterings.sessionclusterings.CompositeSessionClustering import CompositeSessionClustering

with open(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/config.json', 'r') as f:
    configurationJSON = jsmin.jsmin(f.read())


class Config:
    """
    Clase que permite extraer un valor o array dle archivo de configuracion cargado.
    """
    __parameters = json.loads(configurationJSON)  # objeto json cargado.
    userClusteringsD = {
        "UserLRSHistogram": UserLRSHistogramClustering,
        "UserURLsBelonging": UserURLsBelongingClustering,
        "FullUser": FullUserClustering
    }

    sessionClusteringsD = {
        "SessionLRSBelonging": SessionLRSBelongingClustering,
        "SessionUserClustersBelonging": SessionUserClustersBelongingClustering,
        "FullSession": FullSessionClustering,
        "DirectSession": DirectSessionClustering,
        "CompositeSession": CompositeSessionClustering
    }

    def __init__(self):
        pass

    @classmethod
    def getValue(self, attr, mode=None):
        """Permite obtener el valor de un atributo indicado. Ademas se puede especificar si se desea un 'int' o no.

        Notes
            Requiere que el atributo pedido corresponda a un valor unico. Para obtener arrays usar getArray.

        Parameters
        ----------
        attr : str
            nombre del atributo
        mode : str
            modo de lectura del atributo. Puede ser 'INT' o no estar especificado. En el ultimo caso, retornara un str.

        Returns
        -------
        str | int
            Valor correspondiente al atributo
        """
        if mode is not None:
            if mode == 'INT':
                value = int(self.__parameters[attr])
                assert value > 0
                return value
        return self.__parameters[attr]

    @classmethod
    def getArray(self, attr):
        """Permite obtener los valores de un atributo de tipo array indicado.

        Notes
            Requiere que el atributo pedido corresponda a un array de valores.

        Parameters
        ----------
        attr : str
            nombre del atributo
        Returns
        -------
        [str]
            Lista de valores correspondientes al atributo

        """
        jsonArray = self.__parameters[attr]
        assert len(jsonArray) > 0
        return jsonArray

    @classmethod
    def getDict(self, attr):
        """Permite obtener los valores de un atributo de tipo dict indicado.

        Notes
            Requiere que el atributo pedido corresponda a un diccionario.

        Parameters
        ----------
        attr : str
            nombre del atributo
        Returns
        -------
        {str:*}
            Diccionario correspondientes al atributo. Las llaves siempre seran str. Pero los valores contenidos
            pueden ser array, valores o incluso otros diccionarios.

        """
        jsonDict = self.__parameters[attr]
        assert len(jsonDict) > 0
        return jsonDict

    @classmethod
    def getUserClusteringsConfigD(self):
        """ Retorna dict con configuracion para clusterings de usuario

        Returns
        -------
        dict
            con configuracion de clusterings de usuario
        """

        ucConfD = dict()
        user_clusteringD = Config.getDict("user_clustering")
        for k, v in user_clusteringD.items():
            if k in self.userClusteringsD.keys():
                ucConfD[self.userClusteringsD[k]] = v

        return ucConfD

    @classmethod
    def getSessionClusteringsConfigD(self):
        """ Retorna dict con configuracion para clusterings de sesion

        Returns
        -------
        dict
            con configuracion de clusterings de sesion
        """
        scConfD = dict()
        session_clusteringD = Config.getDict("session_clustering")
        for k, v in session_clusteringD.items():
            if k in self.sessionClusteringsD.keys():
                scConfD[self.sessionClusteringsD[k]] = v

        return scConfD
