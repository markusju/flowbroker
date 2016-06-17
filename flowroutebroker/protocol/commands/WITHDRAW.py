__author__ = 'markus'


from abstractcommand import AbstractCommand
from flowroutebroker.protocol import replies
from flowroutebroker.protocol.exceptions import EvaluationError
from flowroutebroker.protocol.exceptions import SemanticError
import security.commands

from flowroutebroker.protocol import evaluators
import exabgp


class WITHDRAW (AbstractCommand):
    def execute(self, api):

        # DISCARD requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 1:
            raise EvaluationError()

        client_ip = self.requestanalyzer.client_ip
        source = self.requestanalyzer.request_method_args[0]
        param_list = self.requestanalyzer.parameters

        # Init FlowRoute
        flowroute = exabgp.FlowRoute()

        # Does not matter, but flowroute requires it to be set
        flowroute.filter_action = "discard"
        try:
            flowroute.source_address = source
            # We're defaulting to the client's ip fo the destination address...
            flowroute.destination_address = client_ip + "/32"
            evaluators.ParameterEvaluator(flowroute, param_list)
        except ValueError:
            raise SemanticError()

        # Security Checks on Application Layer
        security.commands.check_flowroute(flowroute, client_ip)

        api.withdraw_flow_route(flowroute)

        return replies.Reply200()

    def get_method(self):
        pass
