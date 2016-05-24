__author__ = 'markus'


import exabgp
from flowroutebroker.protocol.exceptions import AuthError


def check_flowroute(flowroute, client_ip):
    if not isinstance(flowroute, exabgp.FlowRoute):
        raise ValueError("Must be of type FlowRoute")

    if flowroute.destination_address != client_ip:
        raise AuthError()
