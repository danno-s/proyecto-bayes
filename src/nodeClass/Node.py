"""

"""

import random
import json
from .MicroNode import MicroNode


class Node(object):

    def __init__(self, str):
        self.id = str[0][0]
        self.profile = str[0][4]
        self.id_url = str[0][3]
        self.microNode = str[0][5]
        self.id_user = str[0][1]
        self.clickdate = str[0][2]
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
                    clickdate=self.clickdate,microNode=self.microNode)
        return json.dumps(Dict)

    def __str__(self):
        return str(self.profile) + self.id_url + str(self.microNode)