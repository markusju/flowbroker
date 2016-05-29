__author__ = 'markus'

from abstractcommand import AbstractCommand
from flowroutebroker.protocol import replies
from flowroutebroker.protocol.exceptions import EvaluationError


class RATELIMIT (AbstractCommand):
    def execute(self, api):

        # RATELIMIT requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 2:
            raise EvaluationError()

        ratelimit = self.requestanalyzer.request_method_args[0]
        source = self.requestanalyzer.request_method_args[1]


        print ratelimit
        print source




        return replies.Reply200()

    def get_method(self):
        pass
