__author__ = 'markus'

from abstractcommand import AbstractCommand
from flowroutebroker.protocol import replies
from flowroutebroker.protocol.exceptions import EvaluationError


class VERSION (AbstractCommand):
    def execute(self, api, config):

        # VERSION requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 0:
            raise EvaluationError()

        return replies.Reply200("blah", {"asdasd": "2323"})

        version = api.get_version()

        return replies.Reply200(version)

    def get_method(self):
        pass
