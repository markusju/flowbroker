__author__ = 'markus'

from abc import ABCMeta, abstractmethod

class AbstractReply:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def get_code(self):
        pass

    def to_str(self):
        return str(self.get_code())+" "+str(self.get_message())

    def __str__(self):
        return self.to_str()
