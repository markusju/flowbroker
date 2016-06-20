__author__ = 'markus'

from flowroutebroker.protocol.replies import AbstractReply
from mac import MessageAuthenticationCode
from flowroutebroker.protocol.requestanalyzer import RequestAnalyzer
import datetime
from flowroutebroker.protocol.exceptions import AuthError


class MacHandler:

    def __init__(self, secret):
        """
        Returns an object, which can be integrated into the protocol processing chain.
        Adds Signatures to Requests and verifies Signatures in Requests
        :param secret:
        :return:
        """
        self.mac = MessageAuthenticationCode(secret)

    def apply_to_reply(self, reply):
        """
        Applies a Signature (HMAC) to the Reply
        """
        if not isinstance(reply, AbstractReply):
            raise ValueError("reply must be of type AbstractReply")
        reply.add_parameter("Date", str(datetime.datetime.utcnow().isoformat()))
        signature = self.mac.get_mac_for_message(reply.to_str(True))
        reply.add_parameter("Signature", signature)

    def check_request(self, request):
        """
        Checks the Signature in a incoming Request
        :param request:
        :return:
        """
        if not isinstance(request, RequestAnalyzer):
            raise ValueError("request must be instance of RequestAnalyzer")

        try:
            date = request.parameters["Date"]
            signature = request.parameters["Signature"]

            self.mac.check_mac_for_message(signature, request.to_string_for_signature_validation())


        except KeyError:
            raise AuthError()

