__author__ = 'markus'


import exabgp
from flowroutebroker.protocol.exceptions import SemanticError


class ParameterEvaluator:
    """
    Evaluation of ProtocolParameters
    Applies Parameters from FlowBroker Protocol to a flowroute
    """

    def __init__(self, flowroute, param_list):
        if not isinstance(flowroute, exabgp.FlowRoute):
            raise ValueError("flowroute must be of type FlowRoute")

        self.flowroute = flowroute

        self.param_list = param_list
        self.params = {
            "Destination-Address": self.__destination_address,
            "Port": self.__port,
            "Source-Port": self.__source_port,
            "Destination-Port": self.__destination_port,
            "Protocol": self.__protocol,
            "Unsupported": self.__unsuported
        }

        self.__process()

    def __process(self):
        """
        Processes a request's parameters
        :return:
        """
        for paramkey, paramvalue in self.param_list.items():
            if paramkey not in self.params:
                self.params["Unsupported"](paramvalue)
                continue

            self.params[paramkey](paramvalue)

    def __destination_address(self, value):
        self.flowroute.destination_address = value

    def __port(self, value):
        self.flowroute.port = value

    def __source_port(self, value):
        self.flowroute.source_port = value

    def __destination_port(self, value):
        self.flowroute.destination_port = value

    def __protocol(self, value):
        self.flowroute.protocol = value

    def __unsuported(self, value):
        pass


