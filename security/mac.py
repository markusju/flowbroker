__author__ = 'markus'

import hmac
import hashlib
from flowroutebroker.protocol.exceptions import AuthError


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

    def check_mac_for_message(self, supplied_mac, message):
        """
        Checks the validity of the MAC for a given message
        :param supplied_mac:
        :param message:
        :return:
        """
        # Avoid timing attacks...
        calc_mac = self.get_mac_for_message(message)
        if not hmac.compare_digest(supplied_mac, calc_mac):
            raise AuthError()
        pass
