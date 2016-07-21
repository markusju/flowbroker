__author__ = 'markus'


from abstractcommand import AbstractCommand
from exabgpbrokerserver.flowroutebroker.protocol import replies


class UNSUPPORTED(AbstractCommand):
    def execute(self, api, config):
        return replies.Reply501()

    def get_method(self):
        raise NotImplementedError

    def evaluate(self):
        pass