__author__ = 'markus'

from flowroutebroker.protocol.replies import AbstractReply
from mac import MessageAuthenticationCode
import datetime


class MacHandler:

    def __init__(self, secret):
        self.mac = MessageAuthenticationCode(secret)

    def apply_to_reply(self, reply):
        """
        Applies a Signature (HMAC) to the Reply
        """
        if not isinstance(reply, AbstractReply):
            raise ValueError("reply must be of type AbstractReply")
        reply.add_parameter("Date", str(datetime.datetime.utcnow()))
        signature = self.mac.get_mac_for_message(reply.to_str(True))
        reply.add_parameter("Signature", signature)

    def check_request(self, request):
        """
        Checks the Signature in a incoming Request
        :param request:
        :return:
        """
        pass
