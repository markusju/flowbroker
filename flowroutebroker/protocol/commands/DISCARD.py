__author__ = 'markus'

from abstractcommand import AbstractCommand
from .. import replies
from ..exceptions import EvaluationError


class DISCARD (AbstractCommand):
    def execute(self, api):
        # DISCARD requires at least one Request Method Argument
        if len(self.requestanalyzer.request_method_args) != 1:
            raise EvaluationError()




        return replies.Reply200().to_str()


    def get_method(self):
        pass
