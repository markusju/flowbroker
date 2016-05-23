__author__ = 'markus'

from abstractreply import AbstractReply


class Reply400(AbstractReply):

    def get_message(self):
        return "BAD REQUEST"

    def get_code(self):
        return 400
