__author__ = 'markus'

from abstractreply import AbstractReply


class Reply401(AbstractReply):

    def get_message(self):
        return "UNAUTHORIZED"

    def get_code(self):
        return 401
