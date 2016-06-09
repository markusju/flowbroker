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
            "TCP-Flags": self.__tcp_flags,
            "ICMP-Type": self.__icmp_type,
            "ICMP-Code": self.__icmp_code,
            "Fragment": self.__fragment,
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
        self.flowroute.destination_address = self.read_parameter(value)

    def __port(self, value):
        self.flowroute.port = self.read_parameter(value)

    def __source_port(self, value):
        self.flowroute.source_port = self.read_parameter(value)

    def __destination_port(self, value):
        self.flowroute.destination_port = self.read_parameter(value)

    def __protocol(self, value):
        self.flowroute.protocol = self.read_parameter(value)

    def __tcp_flags(self, value):
        pass

    def __icmp_type(self, value):
        pass

    def __icmp_code(self, value):
        pass

    def __fragment(self, value):
        pass

    def __unsuported(self, value):
        pass

    def read_parameter(self, val):
        """
        Reads the value of Paramters in a request.
        Returns a String for non-seperated values and lists for seperated values
        :param val:
        :return:
        """
        if ";" in val:
            return str.split(val, ",")
        else:
            return val