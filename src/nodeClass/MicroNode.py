# -*- coding: utf-8 -*-

class MicroNode:
    """
    Clase MicroNode, representa los micro estados del modelo.

    Contienen informacion sobre distintos elementos de la pagina: textareas,
    selects, multiselects, radius, y otros,
    """

    def __init__(self, micro_id,macro_id,TextAreas,InputText,RadioButton,Selects,Checkbox, key):
        self.key = key
        self.micro_id = micro_id
        self.macro_id = macro_id
        self.textArea = []
        self.inputText = []
        self.radioButton = []
        self.selects = []
        self.checkbox = []
        if TextAreas and TextAreas != '':
            self.textArea = [int(x) for x in TextAreas.split(" ")]
        if InputText and InputText != '':
            self.inputText = [int(x) for x in InputText.split(" ")]
        if RadioButton and RadioButton != '':
            self.radioButton = [int(x) for x in RadioButton.split(" ")]
        if Selects and Selects != '':
            if '-' in Selects:
                self.selects =[[int(y) for y in x.split("-")]
                             for x in Selects.split(" ")]
            else:
                self.selects = [int(x) for x in Selects.split(" ") if x is not '']
        if Checkbox and Checkbox != '':
            self.checkbox = [[int(y) for y in x.split("-")]
                             for x in Checkbox.split(" ")]


    # def define(self, textArea = None, select = None, multi = None, radius = None, other = None):
    #     """
    #     Define los parametros del micro estado
    #
    #     Parameters
    #     ----------
    #     textArea : List
    #         Vector binario con el estado de los objectos textarea
    #     select : List
    #         Vector binario con el estado de los objectos select
    #     multi : List
    #         Vector binario con el estado de los objectos multiselect
    #     radius : List
    #         Vector binario con el estado de los objectos radius
    #     other : ?
    #         Vector con el estado de otros objetos de la pagina
    #     """
    #     self.textArea = textArea
    #     self.select = select
    #     self.multiSelect = multi
    #     self.radius = radius
    #     self.other = other

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
            if not self.__switch(item, self) == self.__switch(item, micro):
                return False
        return True

    # def __str__(self):
    #     """
    #     Representacion del micro estado como string
    #
    #     Returns
    #     -------
    #     string
    #         El string que representa al micro estado
    #     """
    #     L = self.textArea.copy()
    #     L.extend(self.select)
    #     L.extend(self.multiSelect)
    #     L.extend(self.radius)
    #     L.extend(self.other)
    #     return "".join([str(x) for x in L])

    def toDict(self):
        """
        Representacion del micro estado como diccionario

        Returns
        -------
        Dict
            El diccionario que representa a este micro estado
        """
        Dict = dict(key=self.key, id=self.micro_id, textArea=self.textArea, inputText=self.inputText,
                    radioButton=self.radioButton, selects=self.selects, checkbox=self.checkbox)
        return Dict

    def toList(self):
        L = self.textArea.copy()
        L.extend(self.inputText)
        L.extend(self.radioButton)
        L.extend(self.selects)
        L.extend([item for sublist in self.checkbox for item in sublist])

        return L

    def __switch(self, case, micro):
        switcher = {
            "textArea": micro.textArea,
            "inputText": micro.inputText,
            "radioButton": micro.radioButton,
            "selects": micro.selects,
            "checkbox": micro.checkbox
        }
        return switcher.get(case, "nothing")

