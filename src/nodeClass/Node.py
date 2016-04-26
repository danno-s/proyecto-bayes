# -*- coding: utf-8 -*-

"""
Clase Node, representa un Nodo (paso) de una sesión
"""

import json


class Node(object):

    def __init__(self, sqlStr=None, node_id=None, user_id=None, profile=None, urls_id=None, microNode=None):
        """

        Parameters
        ----------
        sqlStr
        node_id
        user_id
        profile
        urls_id
        microNode

        Returns
        -------

        """
        if sqlStr:
            self.id = sqlStr[0]
            self.user_id = sqlStr[1]
            self.clickdate = sqlStr[2]
            self.urls_id = sqlStr[3]
            self.profile = sqlStr[4]
            self.microNode = sqlStr[5]
        if node_id:
            self.id = node_id
        if user_id:
            self.user_id = user_id
        if urls_id:
            self.urls_id = urls_id
        if profile:
            self.profile = profile
        if microNode:
            self.microNode = microNode
        self.next = None

    def defMicroNode(self, micro_id):
        self.microNode = micro_id

    def addNext(self, node):
        self.next = node

    def belongs(self, node):
        return self.profile == node.profile and self.urls_id == node.urls_id

    def equal(self, node):
        return self.belongs(node) and self.microNode.equal(node.microNode)

    def toJson(self):
        Dict = dict(id_node=self.id, user_id=self.user_id, profile=self.profile, urls_id=self.urls_id,
                    clickdate=self.clickdate, microNode=self.microNode.toDict())
        return json.dumps(Dict)

    def __str__(self):
        return str(self.profile) + ":(" + str(self.urls_id) + "," + str(self.microNode) + ")"
# TODO@ConstanzaEscobar: documentar bien esta clase.
