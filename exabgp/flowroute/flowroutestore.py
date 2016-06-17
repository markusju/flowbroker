__author__ = 'markus'

import time

class FlowRouteStore:
    def __init__(self):
        self.store = []

    def __get_timestamp(self):
        return int(time.time())

    def add_flowroute(self, flowroute):
         self.store.append(flowroute)

    def get_all_flowroutes(self):
        return self.store

    def remove_flowroute(self, flowroute):
        self.store.remove(flowroute)

    def get_expired_flowroutes(self):
        return [elem for elem in self.store if elem.expires <= self.__get_timestamp() and elem.expires > 0]