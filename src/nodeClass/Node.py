"""

"""

import random
import json
from .MicroNode import MicroNode


class Node(object):

    def __init__(self, str=None,id=None, id_user=None,profile=None,id_url=None,microNode= None):
        if str:
            self.id = str[0][0]
            self.id_user = str[0][1]
            self.clickdate = str[0][2]
            self.id_url = str[0][3]
            self.profile = str[0][4]
            self.microNode = str[0][5]
        if id:
            self.id = id
        if id_user:
            self.id_user = id_user
        if id_url:
            self.id_url = id_url
        if profile:
            self.profile = profile
        if microNode:
            self.microNode = microNode
        self.next = None

    def defMicroNode(self, id):
        self.microNode = id

    def addNext(self, node):
        self.next = node

    def belongs(self, node):
        return self.profile == node.profile and self.id_url == node.id_url

    def equal(self, node):
        return self.belongs(node) and self.microNode.equal(node.microNode)

    def toJson(self):
        Dict = dict(id_node=self.id, id_user=self.id_user, profile=self.profile, id_url=self.id_url,
                    clickdate=self.clickdate,microNode=self.microNode.toDict())
        return json.dumps(Dict)

    def __str__(self):
        return str((self.profile, self.id_url,self.microNode))