#!/usr/bin/python
__author__ = 'markus'

import time
import exabgp
import flowroutebroker
from flowroutebroker.config import ConfigError


try:

    api = exabgp.getApi()

    server = flowroutebroker.Server(api)
    server.start()


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            server.stop_server()
            break


except ConfigError as e:
    print "You have an error in your configuration file, exiting."
    print e.message

except Exception as e:
    print "An error occured, exiting."
    print e.message

else:
    print "An error occured, exiting."

finally:
    exit()




"""

flow = exabgp.FlowRoute()
flow.filter_action = "discard"
flow.source_address = "1.1.1.1/32"
flow.protocol = "tcp"
flow.destination_port = "80"

flow2 = exabgp.FlowRoute()
flow2.source_address = "1.1.1.1/32"
flow2.filter_action = "discard"


while True:
    time.sleep(1)
    time.sleep(10)
    #api.withdraw_flow_route(flow)
    time.sleep(500)
"""