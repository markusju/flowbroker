__author__ = 'markus'

import hmac
import hashlib

from exabgpbrokerserver.flowroutebroker.protocol.exceptions import AuthError


class MessageAuthenticationCode:

    def __init__(self, secret):
        """
        Instantiates an instance of the MessageAuthenticationCode Class
        Allows for both checking and generating Hash-Codes based on a given secret.
        :param secret:
        :return:
        """
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

        calc_mac = self.get_mac_for_message(message)
        # Avoid timing attacks...
        if not hmac.compare_digest(supplied_mac, calc_mac):
            raise AuthError()
        pass
