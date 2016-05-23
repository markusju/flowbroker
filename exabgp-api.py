#!/usr/bin/python
__author__ = 'markus'

import time
import exabgp
import flowroutebroker

api = exabgp.getApi()
server = flowroutebroker.Server(api)
server.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        server.stop_server()
        break
exit()








"""
flow = exabgp.FlowRoute()
flow.filter_action = "discard"
flow.source_address = "1.1.1.1/32"
flow.protocol = "tcp"

while True:
    time.sleep(1)
    api.announce_flow_route(flow)
    api.get_version()
    time.sleep(10)
    api.withdraw_flow_route(flow)
"""