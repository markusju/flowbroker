__author__ = 'markus'


import exabgp


class ParameterEvaluator:

    def __init__(self, flowroute, param_list):
        if not isinstance(flowroute, exabgp.FlowRoute):
            raise ValueError("flowroute must be of type FlowRoute")

        self.flowroute = flowroute

        self.param_list = param_list
        self.params = {
            "Destination-Address": self.__destination_address,
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

    def __protocol(self, value):
        self.flowroute.protocol = value


    def __unsuported(self, value):
        pass


