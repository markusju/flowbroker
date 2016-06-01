__author__ = 'markus'

from abstractreply import AbstractReply


class Reply401(AbstractReply):

    def get_message(self):
        return "UNAUHTORIZED"

    def get_code(self):
        return 401
