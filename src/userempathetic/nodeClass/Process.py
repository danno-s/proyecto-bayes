class Process:

    def __init__(self, node):
        self.start = node
        self.last = node
        self.fork = None

    def add(self, node):
        self.last.addNext(node)
        self.last = node
        if len(node.next) > 1:
            self.fork = node

    def isIn(self, node, mode=0):
        step = self.start
        if mode:
            while step is not None:
                if step.equals(node):
                    return True
        else:
            while step is not None:
                if step.belongs(node):
                    return True
        return False
