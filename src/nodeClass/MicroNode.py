"""
Clase MicroNode, representan los micro estados del modelo.

Contienen información sobre distintos elementos de la pagina: textareas,
selects, multiselects, radius, y otros,
"""

import json


class MicroNode:

    def __init__(self, defn):
        """
        Constructor de la clase MicroNode

        Parameters
        ----------
        defn : Tuple
            Tupla con los elementos clave que definen al micro estado.
            Los elementos son strings, y pueden ser "text", "select", "multi",
            "radius" u "other"
        """
        self.key = defn
        self.textArea = []
        self.select = []
        self.multiSelect = []
        self.radius = []
        self.other = None

    def define(self, textArea = None, select = None, multi = None, radius = None, other = None):
        """
        Define los parametros del micro estado

        Parameters
        ----------
        textArea : List
            Vector binario con el estado de los objectos textarea
        select : List
            Vector binario con el estado de los objectos select
        multi : List
            Vector binario con el estado de los objectos multiselect
        radius : List
            Vector binario con el estado de los objectos radius
        other : ?
            Vector con el estado de otros objetos de la pagina
        """
        self.textArea = textArea
        self.select = select
        self.multiSelect = multi
        self.radius = radius
        self.other = other

    def equal(self, micro):
        """
        Verifica si dos micro estados son iguales

        Parameters
        ----------
        micro : MicroNode
            El micro estado con el que se compara

        Returns
        -------
        bool
            True si son iguales, False si no.

        """
        for item in self.key:
            if not self.__switch(item,self) == self.__switch(item, micro):
                return False
        return True

    def __str__(self):
        """
        Representacion del micro estado como string

        Returns
        -------
        string
            El string que representa al micro estado
        """
        L = self.textArea.copy()
        L.extend(self.select)
        L.extend(self.multiSelect)
        L.extend(self.radius)
        L.extend(self.other)
        return "".join([str(x) for x in L])

    def toJson(self):
        """
        Representación del micro estado como JSON

        Returns
        -------
        JSON object
            El objeto JSON que representa a este micro estado
        """
        string = "{ key : " + str(self.key) + ","
        string += "text" + str(self.textArea) + ","
        string += "select" + str(self.select) + ","
        string += "multi" + str(self.multiSelect) + ","
        string += "radius" + str(self.radius) + ","
        string += "other" + str(self.other) + "}"
        return json.loads(str)

    def __switch(self, case, micro):
        switcher = {
            "text" : micro.textArea,
            "select" : micro.select,
            "multi" : micro.multiSelect,
            "radius" : micro.radius,
            "other" : micro.other,
        }
        return switcher.get(case, "nothing")