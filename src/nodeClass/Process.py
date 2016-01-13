class Process:

    def __init__(self, node):
        self.start = node
        self.fork = []

    def add(self, node):
        self.start.addNext(node)

    def addFork(self, process):
        self.start.addNext(process)
        self.fork.append(process.start)