__author__ = 'markus'

from abstractreply import AbstractReply


class Reply500(AbstractReply):
    def get_message(self):
        return "INTERNAL SERVER ERROR"

    def get_code(self):
        return 500
