__author__ = 'markus'

from abstractreply import AbstractReply


class Reply404(AbstractReply):

    def get_message(self):
        return "NOT FOUND"

    def get_code(self):
        return 404
