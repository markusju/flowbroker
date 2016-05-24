__author__ = 'markus'


from abstractcommand import AbstractCommand
from .. import replies


class UNSUPPORTED(AbstractCommand):
    def execute(self, api):
        return replies.Reply501().to_str()

    def get_method(self):
        raise NotImplementedError

    def evaluate(self):
        pass