"""

"""

import random
import json
from .MicroNode import MicroNode


class Node(object):

    def __init__(self, str=None,id=None, user_id=None,profile=None,urls_id=None,microNode= None):
        if str:
            self.id = str[0]
            self.user_id = str[1]
            self.clickdate = str[2]
            self.urls_id = str[3]
            self.profile = str[4]
            self.microNode = str[5]
        if id:
            self.id = id
        if user_id:
            self.user_id = user_id
        if urls_id:
            self.urls_id = urls_id
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
        return self.profile == node.profile and self.urls_id == node.urls_id

    def equal(self, node):
        return self.belongs(node) and self.microNode.equal(node.microNode)

    def toJson(self):
        Dict = dict(id_node=self.id, user_id=self.user_id, profile=self.profile, urls_id=self.urls_id,
                    clickdate=self.clickdate,microNode=self.microNode.toDict())
        return json.dumps(Dict)

    def __str__(self):
        return str(self.profile)+":("+ str(self.urls_id)+","+str(self.microNode)+")"