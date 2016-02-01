class SessionBuffer:

    def __init__(self):
        self.session = list()

    def at(self,i):
        return self.session[i]

    def remove(self,i):
        self.session.remove(self.session[i])

    def append(self, other):
        self.session.append(other)

    def last(self):
        return self.session[-1]

    def first(self):
        return self.session[0]

    def dump(self):
        res = self.session.copy()
        self.empty()
        return res

    def __len__(self):
        return len(self.session)

    def empty(self):
        self.session.clear()

    def isEmpty(self):
        return len(self.session)==0

    def __str__(self):
        return ' '.join([str(s) for s in self.session])