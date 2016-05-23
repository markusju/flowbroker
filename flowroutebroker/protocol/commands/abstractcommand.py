__author__ = 'markus'

from abc import ABCMeta, abstractmethod

class AbstractCommand:
    __metaclass__ = ABCMeta


    @abstractmethod
    def evaluate(self):
        pass

    def execute(self, api):
        pass