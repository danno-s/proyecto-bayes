class SessionBuffer:
    """
    Clase que define un buffer de sesiones.
    """

    def __init__(self):
        """Constructor que inicia list del buffer

        Returns
        -------

        """
        self.session = list()

    def at(self, i):
        """ Permite obtener elemento i del buffer.

        Parameters
        ----------
        i : int
            indice del elemento del buffer a obtener.

        Returns
        -------
        (int,int) | other
            Tupla de IDs de un nodo de una sesion. O alguna otra forma de representacion de los nodos.
        """
        return self.session[i]

    def remove(self, i):
        """Permite remover elemento i del buffer.

        Parameters
        ----------
        i : int
            indice del elemento del buffer a remover.

        Returns
        -------

        """
        self.session.remove(self.session[i])

    def append(self, other):
        """ Agrega el elemento indicado en other al final del buffer.

        Parameters
        ----------
        other : (int,int) | otra representacion
            un nodo de sesion
        Returns
        -------

        """
        self.session.append(other)

    def last(self):
        """ Permite obtener el ultimo elemento del buffer

        Returns
        -------
        (int,int) | otra representacion
            Retorna el nodo de sesion que se encuentra al final del buffer.
        """
        return self.session[-1]

    def first(self):
        """ Permite obtener el primer elemento del buffer

        Returns
        -------
        (int,int) | otra representacion
            Retorna el nodo de sesion que se encuentra al principio del buffer.
        """
        return self.session[0]

    def dump(self):
        """ Retorna todo el contenido del buffer y luego lo vacia.

        Returns
        -------
        List
            Elementos del buffer.
        """
        res = self.session.copy()
        self.empty()
        return res

    def __len__(self):
        """ Permite obtener el largo del buffer.

        Returns
        -------
        int
            Cantidad de elementos cargados en el buffer
        """
        return len(self.session)

    def empty(self):
        """ Borra todo el contenido del buffer.

        Notes
            Los elementos del buffer no son retornados, para esta funcionalidad utilizar dumps.

        Returns
        -------

        """
        self.session.clear()

    def isEmpty(self):
        """ Permite verificar si el buffer esta vacio o no.

        Returns
        -------
        bool
            True si el buffer esta vacio. False si no.
        """
        return len(self.session) == 0

    def __str__(self):
        """ Representacion en str de la sesion almacenadas en el buffer.

        Returns
        -------
        str
            Elementos del buffer separados por espacios.
        """
        return ' '.join([str(s) for s in self.session])
