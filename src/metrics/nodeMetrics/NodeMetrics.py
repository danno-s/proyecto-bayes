# -*- coding: utf-8 -*-

"""
Definicion de distintas Distance (implementacicones de NodeMetric) que comparan dos nodos.
"""
from src.metrics.Metric import NodeMetric
from src.utils.comparatorUtils import getMicroNode, getURLsTree
import json


class MacroDistance(NodeMetric):
    """
    Clase que implementa la metrica como una heuristica calculada en base a los arboles de URLs del macro estado
    de los nodos.
    """

    def __init__(self):
        NodeMetric.__init__(self)

    def distance(self, n1, n2):
        """ Distancia calculada como

        Parameters
        ----------
        n1 : Node
            un nodo
        n2 : Node
            un nodo

        Returns
        -------
        float
            distancia calculada.
        """
        u1 = json.loads(getURLsTree(n1[0]))
        u2 = json.loads(getURLsTree(n2[0]))
        print(u1['value'])
        uset1 = set()
        uset2 = set()
        res = 0.
        self.getURLs(u1, uset1)
        self.getURLs(u2, uset2)
        print(sorted(uset1))
        print(sorted(uset2))
        for i in sorted(uset1):
            if i not in sorted(uset2):
                res += 1.
        return res

    def getURLs(self, d, urlset):
        if d['value'] is not '':
            urlset.add(d['value'].split('?')[0].split(
                '#')[0])  # Filtra parametros de URL
            # TODO: USAR urllib.parse OBTENER LOS PARaMETROS y COMPARAR TANTO LA URL BASE COMO LOS PARaMETROS != que hay.
            # urlset.add(d['value'])
        if d['children'] is not '':
            for child in d['children']:
                self.getURLs(child, urlset)

    # URLs = [json.loads(x[0]) for x in rows]  # Obtiene arboles completos de
    # URLs del sitio en las capturas"

    # TODO: filtrar parametros de urls ?asdsa=23 .. etc.

    # for i,urltree in enumerate(URLs):
    #   print("ARBOL DE URL N"+str(i+1)+": " + json.dumps(urltree, indent=4))

    # Funcion para encontrar URLs unicas dentro de un mismo arbol:

    # def getURLs(d, urlset):
    #    for k,v in d.items():
    #        urlset.add(k)
    #        if len(v) is not 0:
    #            for urlT in v:
    #                if isinstance(urlT, dict):
    #                    getURLs(urlT, urlset)
    #                else:
    #                    urlset.add(urlT.keys())
    #
    # allurls = set()
    # for urltr in URLs:
    #    getURLs(urltr,allurls)
    #
    # print("TOTAL URLs FOUND ("+str(len(allurls))+"): "+ str(allurls))


class MicroDistance(NodeMetric):
    """
    Clase que implementa la metrica como una heuristica calculada en base a los vectores de ciertos contentElements del
    micro estado de los nodos.
    """

    def __init__(self):
        NodeMetric.__init__(self)

    def distance(self, n1, n2):
        """ Distancia calculada como la suma de las diferencias de los vectores de los contentElements. Sin incluir
        los checkboxs.

        Notes
            En algunos casos como selects y radioButtons no se ve la diferencia si no que la cantidad de elementos
            diferentes.

        Parameters
        ----------
        n1 : Node
            un nodo
        n2 : Node
            un nodo

        Returns
        -------
        float
            distancia calculada.
        """

        mn1 = getMicroNode(n1[1])
        mn2 = getMicroNode(n2[1])

        iT_d = self.__inputTextDistance(mn1.inputText, mn2.inputText)
        sel_d = self.__selectsDistance(mn1.selects, mn2.selects)
        # ch_d = self.__checkboxDistance(n1.checkbox,n2.checkbox)
        tA_d = self.__textAreaDistance(mn1.textArea, mn2.textArea)
        rB_d = self.__radioButtonDistance(mn1.radioButton, mn2.radioButton)
        #print("INPUTTEXT DISTANCE=" + str(iT_d))
        #print("SELECTS DISTANCE=" + str(sel_d))
        #print("TEXTAREAS DISTANCE=" + str(tA_d))
        #print("RADIOBUTTONS DISTANCE=" + str(tA_d))
        # print("CHECKBOXS DISTANCE="+str(ch_d))
        return float(sel_d + iT_d + tA_d + rB_d)

    def __inputTextDistance(self, t1, t2):
        #print("inputTexts:" + "\t" + str(t1) + "\t" + str(t2))
        return sum([abs(x - y) for x, y in zip(t1, t2)])

    def __selectsDistance(self, sel1, sel2):
        #print("selects:" + "\t" + str(sel1) + "\t" + str(sel2))
        res = 0
        if any(isinstance(i, list) for i in sel1) and any(isinstance(i, list) for i in sel2):
            for selGroup1, selGroup2 in zip(sel1, sel2):
                res += sum([int(x != y) for x, y in zip(selGroup1, selGroup2)])
        else:
            res = sum([int(x != y) for x, y in zip(sel1, sel2)])
        return res

    """
    #TODO: MODIFICAR CAPTURA DE CHECKBOXES PARA NORMALIZAR VECTORES.
    #TODO: ACTUALMENTE LOS GRUPOS CAMBIAN SU CANTIDAD DE ELEMENTOS, HACIENDOLOS IMPOSIBLES DE COMPARAR.
    def __checkboxDistance(self,ch1,ch2):
        print("checkboxs:" +"\t"+str(ch1)+"\t"+str(ch2))
        res = 0
        for chGroup1,chGroup2 in zip(ch1,ch2):
            res += sum([int(x != y) for x, y in zip(chGroup1, chGroup2)])
        return res
    """

    def __textAreaDistance(self, t1, t2):
        #print("textAreas:" + "\t" + str(t1) + "\t" + str(t2))
        return sum([abs(x - y) for x, y in zip(t1, t2)])

    def __radioButtonDistance(self, r1, r2):
        #print("radioButtons:" + "\t" + str(r1) + "\t" + str(r2))
        return sum([abs(x - y) for x, y in zip(r1, r2)])
