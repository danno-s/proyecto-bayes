"""
Módulo para cargar configuración desde un archivo "config.json" en el path del proyecto.
"""

import json
import os
import jsmin

with open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/config.json', 'r') as f:
    configurationJSON = jsmin.jsmin(f.read())


class Config:
    """
    Clase que permite extraer un valor o array dle archivo de configuración cargado.
    """
    __parameters = json.loads(configurationJSON)  # objeto json cargado.

    def __init__(self):
        pass

    @classmethod
    def getValue(self, attr, mode=None):
        """Permite obtener el valor de un atributo indicado. Además se puede especificar si se desea un 'int' o no.

        Notes
            Requiere que el atributo pedido corresponda a un valor único. Para obtener arrays usar getArray.

        Parameters
        ----------
        attr : str
            nombre del atributo
        mode : str
            modo de lectura del atributo. Puede ser 'INT' o no estar especificado. En el último caso, retornará un str.

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
