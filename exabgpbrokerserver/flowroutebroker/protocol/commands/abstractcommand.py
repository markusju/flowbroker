__author__ = 'markus'

from abc import ABCMeta, abstractmethod

from exabgpbrokerserver.flowroutebroker.protocol.requestanalyzer import RequestAnalyzer


class AbstractCommand:
    __metaclass__ = ABCMeta

    def __init__(self, requestanalyzer):
        if not isinstance(requestanalyzer, RequestAnalyzer):
            raise ValueError("Argument must be instance of RequestAnalyzer")
        self.requestanalyzer = requestanalyzer

    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def execute(self, api, config):
        pass