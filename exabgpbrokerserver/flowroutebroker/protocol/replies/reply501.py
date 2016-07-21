__author__ = 'markus'

from abstractreply import AbstractReply


class Reply501(AbstractReply):
    def get_message(self):
        return "NOT IMPLEMENTED"

    def get_code(self):
        return 501
