"""

"""

import random
import json
from .MicroNode import MicroNode


class Node(object):

    def __init__(self, profile, url, micro=()):
        self.profile = profile
        self.url = url
        self.microNode = MicroNode(micro)
        self.next = []

    def defMicroNode(self, state):
        self.microState = state

    def addNext(self, node):
        self.next.append(node)

    def belongs(self, node):
        return self.profile == node.profile and self.url == node.url

    def equals(self, node):
        return self.equal(node) and self.microNode.equal(node.microState)

    def toJson(self):
        string = "{ id : " + random.randint() + "," #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        string += "profile : " + str(self.profile) + ","
        string += "url : " + self.url + ","
        string += "MicroNode : " + json.dumps(self.microNode.toJson()) + "}"
        return json.loads(string)

    def __str__(self):
        return str(self.profile) + self.url + str(self.microNode)