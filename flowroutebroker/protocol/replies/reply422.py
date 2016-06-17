__author__ = 'markus'


from abstractreply import AbstractReply


class Reply422(AbstractReply):

    def get_message(self):
        return "SEMANTIC ERRORS"

    def get_code(self):
        return 422
