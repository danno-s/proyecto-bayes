from abc import ABCMeta, abstractmethod


class Feature:
    __metaclass__ = ABCMeta

    def __init__(self): pass

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def toSQLItem(self): pass


class UserFeature(Feature):
    __metaclass__ = ABCMeta

    def __init__(self):
        Feature.__init__(self)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def toSQLItem(self): pass


class SessionFeature(Feature):
    __metaclass__ = ABCMeta

    def __init__(self):
        Feature.__init__(self)

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def toSQLItem(self): pass
