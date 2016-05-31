__author__ = 'markus'


import exabgp
from flowroutebroker.protocol.exceptions import PermError


def check_flowroute(flowroute, client_ip):
    if not isinstance(flowroute, exabgp.FlowRoute):
        raise ValueError("Must be of type FlowRoute")

    if flowroute.destination_address != client_ip+"/32":
        raise PermError()
