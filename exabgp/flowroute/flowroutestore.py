__author__ = 'markus'

import time
import threading



class FlowRouteStore:
    def __init__(self):
        self.store = []
        self.lock = threading.Lock()

    def __get_timestamp(self):
        return int(time.time())

    def add_flowroute(self, flowroute):
        try:
            self.lock.acquire()
            for el in self.store:
                if el == flowroute:
                    el._expires = flowroute.expires
                    return

            self.store.append(flowroute)
        finally:
            self.lock.release()

    def get_all_flowroutes(self):
        try:
            self.lock.acquire()
            return self.store
        finally:
            self.lock.release()

    def remove_flowroute(self, flowroute):
        try:
            self.lock.acquire()
            self.store.remove(flowroute)
            return flowroute
        except ValueError:
            for el in self.store:
                if el.equals_match_crit(flowroute):
                    self.store.remove(el)
                    return el
            raise ValueError("Not Found..")
        finally:
            self.lock.release()

    def get_expired_flowroutes(self):
        try:
            self.lock.acquire()
            return [elem for elem in self.store if self.__get_timestamp() >= elem.expires > 0]
        finally:
            self.lock.release()