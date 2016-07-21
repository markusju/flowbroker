__author__ = 'markus'

from abstractcommand import AbstractCommand
from exabgpbrokerserver.flowroutebroker.protocol import replies
from exabgpbrokerserver.flowroutebroker.protocol.exceptions import EvaluationError
from exabgpbrokerserver.flowroutebroker.protocol.exceptions import SemanticError
import exabgpbrokerserver.flowroutebroker.security.commands

from exabgpbrokerserver.flowroutebroker.protocol import evaluators
from exabgpbrokerserver import exabgp


class DISCARD (AbstractCommand):
    def execute(self, api, config):

        # DISCARD requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 1:
            raise EvaluationError()

        client_ip = self.requestanalyzer.client_ip
        source = self.requestanalyzer.request_method_args[0]
        param_list = self.requestanalyzer.parameters

        # Init FlowRoute
        flowroute = exabgp.FlowRoute()

        flowroute.filter_action = "discard"
        try:
            flowroute.source_address = source
            flowroute.destination_address = client_ip + "/32"
            evaluators.ParameterEvaluator(flowroute, param_list)
        except ValueError:
            raise SemanticError()

        # Security Checks
        exabgpbrokerserver.flowroutebroker.security.commands.check_flowroute(flowroute, client_ip, config)

        api.announce_flow_route(flowroute)

        return replies.Reply200()

    def get_method(self):
        pass
