__author__ = 'markus'

import datetime

import pytz
import dateutil.parser

from exabgpbrokerserver.flowroutebroker.protocol.replies import AbstractReply
from mac import MessageAuthenticationCode
from exabgpbrokerserver.flowroutebroker.protocol.requestanalyzer import RequestAnalyzer
from exabgpbrokerserver.flowroutebroker.protocol.exceptions import AuthError


class MacHandler:

    def __init__(self, secret, config):
        """
        Returns an object, which can be integrated into the protocol processing chain.
        Adds Signatures to Requests and verifies Signatures in Requests
        :param secret:
        :return:
        """
        self.mac = MessageAuthenticationCode(secret)
        self.config = config

    def apply_to_reply(self, reply):
        """
        Applies a Signature (HMAC) to the Reply
        """
        if not isinstance(reply, AbstractReply):
            raise ValueError("reply must be of type AbstractReply")
        reply.add_parameter("Date", str(datetime.datetime.utcnow().isoformat())+"Z")
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


            now = datetime.datetime.utcnow()
            now = now.replace(tzinfo=pytz.utc)

            yourdate = dateutil.parser.parse(date)

            diff = now-yourdate


            if diff.total_seconds() > (self.config.get_tolerance() / 1000.0) or diff.total_seconds() < -(self.config.get_tolerance() / 1000.0):
                raise AuthError()

            self.mac.check_mac_for_message(signature, request.to_string_for_signature_validation())


        except KeyError:
            raise AuthError()

        except ValueError:
            raise AuthError()

