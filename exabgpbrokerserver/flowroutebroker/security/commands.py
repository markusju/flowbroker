__author__ = 'markus'

from exabgpbrokerserver import exabgpmods
from exabgpbrokerserver.flowroutebroker.protocol.exceptions import PermError


def check_flowroute(flowroute, client_ip, config):
    if not isinstance(flowroute, exabgpmods.FlowRoute):
        raise ValueError("Must be of type FlowRoute")

    if not config.is_destination_permitted(client_ip, flowroute.destination_address):
        raise PermError()

    # Withdraw may not contain an expiration setting
    if flowroute.filter_action == "withdraw" and flowroute.expires != 0:
        flowroute._expires = 0


