__author__ = 'markus'

from abstractcommand import AbstractCommand
from flowroutebroker.protocol import replies
from flowroutebroker.protocol.exceptions import EvaluationError


class VERSION (AbstractCommand):
    def execute(self, api):

        # RATELIMIT requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 0:
            raise EvaluationError()

        if len(self.requestanalyzer._request_method_args) != 0:
            raise EvaluationError()

        return replies.Reply200("blah").to_str()

        version = api.get_version()

        return replies.Reply200(version).to_str()

    def get_method(self):
        pass
