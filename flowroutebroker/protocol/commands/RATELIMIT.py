import exabgp
import flowroutebroker

__author__ = 'markus'

from abstractcommand import AbstractCommand
from flowroutebroker.protocol import replies
from flowroutebroker.protocol.exceptions import EvaluationError, SemanticError
import flowroutebroker.security.commands
from flowroutebroker.protocol import evaluators


class RATELIMIT (AbstractCommand):
    def execute(self, api, config):

        # RATELIMIT requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 2:
            raise EvaluationError()

        ratelimit = self.requestanalyzer.request_method_args[0]
        source = self.requestanalyzer.request_method_args[1]
        param_list = self.requestanalyzer.parameters
        client_ip = self.requestanalyzer.client_ip

        # Init FlowRoute
        flowroute = exabgp.FlowRoute()

        try:
            flowroute.filter_action = "rate-limit "+ratelimit
            flowroute.source_address = source
            flowroute.destination_address = client_ip + "/32"
            evaluators.ParameterEvaluator(flowroute, param_list)
        except ValueError:
            raise SemanticError()

        # Security Checks
        flowroutebroker.security.commands.check_flowroute(flowroute, client_ip, config)

        api.announce_flow_route(flowroute)

        return replies.Reply200()

    def get_method(self):
        pass
