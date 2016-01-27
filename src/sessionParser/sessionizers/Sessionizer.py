from src.utils.loadConfig import Config


class Sessionizer:
    def __init__(self):
        self.tlimit = Config().getValue(attr='session_tlimit',mode='INT')


