__author__ = 'markus'

import hmac
import hashlib


class MessageAuthenticationCode:

    def __init__(self, secret):
        self.secret = secret
        pass

    def get_mac_for_message(self, message):
        """
        Provides the Message Authentication Code
        :return:
        """
        return hmac.new(self.secret, message, hashlib.sha256).hexdigest()
