__author__ = 'markus'

from abstractreply import AbstractReply


class Reply200(AbstractReply):

    def get_message(self):
        return "OK"

    def get_code(self):
        return 200
