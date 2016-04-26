#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Extractor de los micro estados del sitio para los datos capturados.
"""
import json


class MicroStateVectorExtractor:
    """
    Clase encargada de extraer los vectores de micro estado del sitio y almacenarlos en un diccionario.
    Los elementos a extraer se definen en el archivo de configuración del sistema.
    """

    def __init__(self):
        """Constructor

        Returns
        -------

        """
        __allFuncs = {
            'TextAreas': self.__getTextAreas,
            'InputText': self.__getInputText,
            'RadioButton': self.__getRadioButtons,
            'Selects': self.__getSelects,
            'Checkbox': self.__getCheckboxes
        }
        from src.utils.loadConfig import Config
        self.elementTypes = sorted(Config().getArray(attr='elementTypes'))
        self.availableTypes = ' / '.join(
            [x for x in sorted(__allFuncs.keys())])
        self.funcD = dict()
        for el_type in self.elementTypes:
            try:
                self.funcD[el_type] = __allFuncs[el_type]
            except KeyError:
                print("Type '" + el_type +
                      "' is not a valid element type for the extractor.")
                print("Please check that the types array in Config.json contains only these:\n" + str(
                    self.getAvailableTypes()))

    def getElementTypes(self):
        """Retorna una lista los tipos de elementos de micro estado a extraer, cargados desde configuración.

        Returns
        -------
        [str]
            tipos de elementos cargados desde configuración.
        """
        return sorted(self.elementTypes)

    def getAvailableTypes(self):
        """Retorna una lista con los tipos de elementos de micro estado que es posible extraer.

        Returns
        -------
        [str]
            tipos de elementos de micro estado que es posible extraer.
        """
        return self.availableTypes

    def __getTextAreas(self, d, L):
        """Agrega a la lista L de entrada el valor de estado del elemento textArea ingresado en d.

        Parameters
        ----------
        d : dict
            diccionario de un elemento de contenido textArea.
        L : list
            vector de estado que contendrá los estados de todos los elementos textArea.

        Returns
        -------
        """
        hasValue = d['HasValue']
        # isHidden = d['IsHidden']
        if True:  # isHidden == 'false' or isHidden == 'true':
            if hasValue == 'true':
                L.append(1)
            else:
                L.append(0)

    def __getInputText(self, d, L):
        """Agrega a la lista L de entrada el valor de estado del elemento inputText ingresado en d.

        Parameters
        ----------
        d : dict
            diccionario de un elemento de contenido inputText.
        L : list
            vector de estado que contendrá los estados de todos los elementos inputText.

        Returns
        -------
        """
        hasValue = d['HasValue']
        isHidden = d['IsHidden']
        if isHidden == 'false' or isHidden == 'true':
            if hasValue == 'true':
                L.append(1)
            else:
                L.append(0)

    def __getRadioButtons(self, d, L):
        """Agrega a la lista L de entrada el valor de estado del elemento radioButton ingresado en d.

        Parameters
        ----------
        d : dict
            diccionario de un elemento de contenido radioButton.
        L : list
            vector de estado que contendrá los estados de todos los elementos radioButton.

        Returns
        -------
        """
        selected = d['Selected']
        L.append(selected)

    def __getSelects(self, d, L):
        """Agrega a la lista L de entrada el valor de estado del elemento select ingresado en d.

        Parameters
        ----------
        d : dict
            diccionario de un elemento de contenido select.
        L : list
            vector de estado que contendrá los estados de todos los elementos select, agrupados si es el caso.

        Returns
        -------
        """
        options = d['Selected']
        if len(options) > 0:
            L.append('-'.join(options))

    def __getCheckboxes(self, d, L):
        """Agrega a la lista L de entrada el valor de estado del elemento checkbox ingresado en d.

        Parameters
        ----------
        d : dict
            diccionario de un elemento de contenido checkbox.
        L : list
            vector de estado que contendrá los estados de todos los elementos checkbox, agrupados si es el caso.

        Returns
        -------
        """
        quantity = int(d['Quantity'])
        vector = ['0'] * quantity
        options = d['Selected']
        if options != '':
            for i in options:
                vector[int(i)] = '1'
        L.append('-'.join(vector))

    def generateStateVectorFrom(self, contentElements, el_type, L):
        """Función recursiva que recorre contentElements y va creando el vectore de estado en L para el tipo de
         elemento indicado en type.

        Parameters
        ----------
        contentElements : dict
            json de elementos de contenido extraido de la captura.
        el_type : str
            tipo de elemento a extraer.
        L : list
            vector de estado que contendrá los estados de todos los elementos del tipo indicado.

        Returns
        -------

        """
        if len(contentElements) == 0:
            return
        valueD = contentElements['value']
        try:
            elementL = valueD[el_type]
        except:
            print(valueD)
            raise
        if elementL != '':
            for el in elementL:
                self.funcD[el_type](el, L)
        children = contentElements['children']
        for child in children:
            self.generateStateVectorFrom(child, el_type, L)

    def getStateVectors(self, contentElements):
        """Función que recorre todos los tipos de elementos cargados en el MicroStateVectorExtractor y los retorna en
        un diccionario.

        Parameters
        ----------
        contentElements : dict
            json de elementos de contenido extraido de la captura.

        Returns
        -------
        dict
            diccionario de vectores de estado obtenidos, que utiliza como llave el str del tipo de elemento.

        """
        data = dict()
        for el_type in self.elementTypes:
            L = list()
            try:
                self.generateStateVectorFrom(contentElements, el_type, L)
                data[el_type] = ' '.join(map(str, L))
            except:
                print(json.dumps(contentElements, indent=2))
                raise
        return data
