__author__ = 'markus'


class PermError (Exception):
    def __init__(self):
        self.message = "Permission Error!"
