from .MicroNode import MicroNode
import random
import json


class Node(object):
    """ Class Node, represents the state of a given process """

    def __init__(self, user, url, micro=()):
        """
        Create new Node Object

        Args:
            user (int): The role of the user
            url (str): The node's url tree
            micro (Optional Tuple): The A tuple with the names of the defining parameters. The names can be
                "text", "select", "multi", "radius" or "other". Defaults to ().
        """
        self.user = user
        self.url = url
        self.microNode = MicroNode(micro)
        self.next = []

    def defMicroNode(self, state):
        """
        Set this Node's MicroNode

        Args:
            state (MicroNode): The Node's MicroNode
        """
        self.microState = state

    def addNext(self, node):
        """
        Add reference to next Node

        Args:
            node (Node): The next Node
        """
        self.next.append(node)

    def belongs(self, node):
        """
        Check if two nodes have the same user and url

        Args:
            node (Node): The node to compare with

        Returns:
            bool: True if both Nodes have the same user and url, False otherwise.
        """
        return self.user == node.user and self.url == node.url

    def equals(self, node):
        """
        Check if two nodes have the same user, url and MicroNode

        Args:
            node (Node): The node to compare with

        Returns:
            bool: True if both Node objects are equal, False otherwise.
        """
        return self.equal(node) and self.microNode.equal(node.microState)

    def toJson(self):
        string = "{ id : " + random.randint() + "," #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        string += "user : " + str(self.user) + ","
        string += "url : " + self.url + ","
        string += "MicroNode : " + json.dumps(self.microNode.toJson()) + "}"
        return json.loads(string)

    def __str__(self):
        return str(self.user) + self.url + str(self.microNode)
