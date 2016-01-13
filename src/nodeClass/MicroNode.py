class MicroNode:
    """ Class MicroNode, represents inner state of a Node """

    def __init__(self, defn):
        """
        Create new MicroNode object

        Args:
            defn (Tuple): A tuple with the names of the defining parameters. The names can be
                "text", "select", "multi", "radius" or "other".

        Returns:
            MicroNode object

        """
        self.key = defn
        self.textArea = []
        self.select = []
        self.multiSelect = []
        self.radius = []
        self.other = None

    def define(self, textArea = None, select = None, multi = None, radius = None, other = None):
        """
        Define Node's attributes

        Args:
            textArea (Optional List[int]): textarea object's vector representation. Defaults to None.
            select (Optional List[int]): selec object's vector representation. Defaults to None.
            multi (Optional List[int]): multiselect object's vector representation. Defaults to None.
            radius (Optional List[int]): radious object's vector representation. Defaults to None.
            other (Optional List[int]): other's vector representation. Defaults to None.

        """
        self.textArea = textArea
        self.select = select
        self.multiSelect = multi
        self.radius = radius
        self.other = other

    def equal(self, micro):
        """
        Check equality between MicroNode objects

        Args:
            micro (MicroNode): The MicroNode to compare with

        Returns:
            bool: True if both MicroNode objects are equal, False otherwise.

        """
        for item in self.key:
            if not self.__switch(item,self) == self.__switch(item, micro):
                return False
        return True

    def __switch(self, case, micro):
        switcher = {
            "text" : micro.textArea,
            "select" : micro.select,
            "multi" : micro.multiSelect,
            "radius" : micro.radius,
            "other" : micro.other,
        }
        return switcher.get(case, "nothing")