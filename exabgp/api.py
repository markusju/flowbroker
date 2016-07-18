__author__ = 'markus'

import time
import threading
import flowroute


class Api(threading.Thread):

    def __init__(self, api):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.api = api
        self.lock = threading.Lock()
        self.flowroutestore = flowroute.FlowRouteStore()

    def run(self):
        """
        Thread method. Checks flowroute Store for expired routes
        :return:
        """
        while True:
            expired_flowroutes = self.flowroutestore.get_expired_flowroutes()


            for el in expired_flowroutes:
                self.withdraw_flow_route(el)

            time.sleep(1)

    def announce_flow_route(self, flowroute):
        """
        Announces a flow route
        :param flowroute:
        :return:
        """
        self.flowroutestore.add_flowroute(flowroute)
        self.api.announce_flow_route(flowroute)

    def withdraw_flow_route(self, flowroute):
        """
        Withdraws a flowroute
        :param flowroute:
        :return:
        """
        flow = self.flowroutestore.remove_flowroute(flowroute)
        self.api.withdraw_flow_route(flow)
