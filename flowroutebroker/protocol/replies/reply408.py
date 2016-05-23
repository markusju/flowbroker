__author__ = 'markus'


from abstractreply import AbstractReply


class Reply408(AbstractReply):

    def get_message(self):
        return "REQUEST TIMED OUT"

    def get_code(self):
        return 408
