__author__ = 'markus'

from abstractreply import AbstractReply


class Reply403(AbstractReply):

    def get_message(self):
        return "FORBIDDEN"

    def get_code(self):
        return 403
