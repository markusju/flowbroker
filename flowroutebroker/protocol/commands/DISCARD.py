__author__ = 'markus'

from abstractcommand import AbstractCommand
from flowroutebroker.protocol import replies
from flowroutebroker.protocol.exceptions import EvaluationError
import security.commands

from flowroutebroker.protocol import evaluators
import exabgp


class DISCARD (AbstractCommand):
    def execute(self, api):
        # DISCARD requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 1:
            raise EvaluationError()

        client_ip = self.requestanalyzer.client_ip

        source = self.requestanalyzer.request_method_args[0]
        param_list = self.requestanalyzer.parameters


        flowroute = exabgp.FlowRoute()
        flowroute.filter_action = "discard"
        flowroute.source_address = source
        flowroute.destination_address = client_ip + "/32"

        evaluators.ParameterEvaluator(flowroute, param_list)

        # Security Checks
        security.commands.check_flowroute(flowroute, client_ip)

        api.announce_flow_route(flowroute)

        return replies.Reply200().to_str()


    def get_method(self):
        pass
