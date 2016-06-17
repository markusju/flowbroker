__author__ = 'markus'

import time
import threading
import flowroute


class Api(threading.Thread):

    def __init__(self, api):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.api = api
        self.flowroutestore = flowroute.FlowRouteStore()

    def run(self):
        while True:
            expired_flowroutes = self.flowroutestore.get_expired_flowroutes()

            for el in expired_flowroutes:
                self.withdraw_flow_route(el)

            time.sleep(1)

    def announce_flow_route(self, flowroute):
        self.flowroutestore.add_flowroute(flowroute)
        self.api.announce_flow_route(flowroute)

    def withdraw_flow_route(self, flowroute):
        self.flowroutestore.remove_flowroute(flowroute)
        self.api.withdraw_flow_route(flowroute)

