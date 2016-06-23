__author__ = 'markus'


import exabgp
from flowroutebroker.protocol.exceptions import PermError


def check_flowroute(flowroute, client_ip, config):
    if not isinstance(flowroute, exabgp.FlowRoute):
        raise ValueError("Must be of type FlowRoute")

    if not config.is_destination_permitted(client_ip, flowroute.destination_address):
        raise PermError()
