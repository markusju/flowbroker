__author__ = 'markus'

import time
import threading
from flowroute import FlowRoute

class Api ():

    def __init__(self, stdinreader, stdoutwriter, maxtries=10, sleeptime=0.01):
        self.stdinreader = stdinreader
        self.stdoutwriter = stdoutwriter
        self.maxtries = maxtries
        self.sleeptime = sleeptime
        self.lock = threading.Lock()

    def get_version(self):
        return self.__execute_command_get_reply("version")

    def announce_flow_route(self, flowroute):
        """
        Pushes a flow route to EXABGP
        :param flowroute:
        :return:
        """
        if not isinstance(flowroute, FlowRoute):
            raise ValueError("Argument must be instance of FlowRoute")
        self.stdoutwriter.addCommand("announce "+flowroute.buildRoute())

    def withdraw_flow_route(self, flowroute):
        if not isinstance(flowroute, FlowRoute):
            raise ValueError("Argument must be instance of FlowRoute")
        self.stdoutwriter.addCommand("withdraw "+flowroute.buildRoute())

    def __execute_command_get_reply(self, cmd):
        try:
            self.lock.acquire()
            numbefore = self.stdinreader.getNumOfLines()
            self.stdoutwriter.addCommand(cmd)
            numnow = self.stdinreader.getNumOfLines()
            tries = 0
            while (numnow <= numbefore):
                numnow = len(self.stdinreader.getLines())
                if (tries > self.maxtries):
                    raise Exception("Exabgp did not answer!")
                tries += 1
                time.sleep(self.sleeptime)
            out = self.stdinreader.getCurrentLine()
        finally:
            self.lock.release()
        return out

