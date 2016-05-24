__author__ = 'markus'


class AuthError (Exception):
    def __init__(self):
        self.message = "Authentication Error!"
