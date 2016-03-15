"""
Modelo de representación de una sesión.
"""

from src.userempathetic.nodeClass.Node import Node


class Session:
    """
    Clase Session, representa una sesión en el sistema
    """
    def __init__(self, sequence, profile="", initTime="", endTime="", user_id="", session_id=None):
        """ Constructor de una Session.

        Parameters
        ----------
        sequence : [tuple]
            lista de tuplas (macro_id, micro_id), o (macro_id, None).
        profile : str
            perfil de usuario que realizó la sesión.
        initTime : datetime | str
            tiempo de inicio de sesión
        endTime : datetime | str
            tiempo de término de sesión
        user_id : int
            id de usuario.
        session_id : int
            id de la sesión.

        Returns
        -------

        """
        self.initTime = initTime
        self.endTime = endTime
        self.user_id = user_id
        self.profile = profile
        self.sequence = sequence
        if session_id:
            self.session_id = session_id

    def __getSequenceFromNode(self, node):
        """Permite obtener una secuencia de nodos a partir de la lista enlazada definida por el primer nodo 'node'

        Parameters
        ----------
        node : Node
            Primer nodo de una sesión.

        Returns
        -------
        [tuple]
            (node.urls_id, None) | (node.urls_id, node.microNode)
        """
        sequence = list()
        while node:
            if node.urls_id:
                if node.microNode:
                    sequence.append((node.urls_id, node.microNode))
                else:
                    sequence.append((node.urls_id, None))
            node = node.next
        return sequence

    def getFirstNode(self, steps=None):
        """Permite obtener un objeto Nodo que representa el inicio de una sesión representada como lista enlazada.

        Parameters
        ----------
        steps : [tuple]
            (urls_id, micro_id) | (urls_id, None)

        Returns
        -------
        a Node object with the nested list of the session.
        """
        if not steps:
            steps = self.sequence

        firstStep = steps[0]
        macro_id = firstStep[0]
        micro_id = firstStep[1]
        firstNode = Node(user_id=self.user_id, profile=self.profile, urls_id=macro_id, microNode=micro_id)
        currentNode = firstNode
        for step in steps[1:]:
            macro_id = step[0]
            micro_id = step[1]
            newNode = Node(user_id=self.user_id, profile=self.profile, urls_id=macro_id, microNode=micro_id)
            currentNode.addNext(newNode)
            currentNode = currentNode.next
        return firstNode

    def accept(self, visitor):
        """
        ????????????????????????????????????????????????????
        Parameters
        ----------
        visitor

        Returns
        -------

        """
        visitor.metSession(self)

    def __str__(self):
        """ Retorna representación de str de esta sesión.

        Returns
        -------
        str
            string con la información de la sesión.
        """
        return str(self.user_id) + " ["+str(self.profile)+"] "+":\t" + self.__sequenceToStr(self.sequence) + " ;\t " + str(
            self.initTime) + " >> " + str(self.endTime)

    def __sequenceToStr(self, sequence):
        """ Retorna la representación de string de una secuencia de nodos.

        Parameters
        ----------
        sequence : [tuple]
            Lista de nodos (macro_id, micro_id)
        Returns
        -------
        str
            string con cadena de pares (macro_id, micro_id)
        """
        tps = list()
        for x in sequence:
            if x[1]:
                tps.append("(" + str(x[0]) + "," + str(x[1]) + ")")
            else:
                tps.append("(" + str(x[0]) + ")")
        s = ' >> '.join(tps)
        return s

    def toSQLItem(self):
        """ Permite transformar la sesión a un item que el sqlWrapper puede escribir en una base de datos.

        Returns
        -------
        str
            string con item (profile, sequence, user_id, inittime, endtime) para el sqlWrapper
        """
        steps = list()
        for x in self.sequence:
            if x[1]:
                step = str(x[0]) + "," + str(x[1])
            else:
                step = str(x[0])
            steps.append(step)
        return (self.profile, ' '.join(steps), self.user_id, self.initTime, self.endTime)
