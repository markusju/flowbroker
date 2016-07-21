__author__ = 'markus'


class NotFoundError (Exception):
    def __init__(self):
        self.message = "Resource could not be found."
