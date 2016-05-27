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
        """
        Returns the version of EXABGP
        :return:
        """
        return self.__execute_command_get_reply("version")

    def announce_flow_route(self, flowroute):
        """
        Pushes a flow route to EXABGP
        :param flowroute:
        :return:
        """
        if not isinstance(flowroute, FlowRoute):
            raise ValueError("Argument must be instance of FlowRoute")
        self.stdoutwriter.addCommand("announce "+flowroute.build_route())

    def withdraw_flow_route(self, flowroute):
        """
        Withdraws a flowroute from EXABGP
        :param flowroute:
        :return:
        """
        if not isinstance(flowroute, FlowRoute):
            raise ValueError("Argument must be instance of FlowRoute")
        self.stdoutwriter.addCommand("withdraw "+flowroute.build_route())

    def __execute_command_get_reply(self, cmd):
        """
        Invokes execution of a command and fetches EXABGP's reply using polling
        Keep in mind that the communication with EXABGP is performed asynchronous
        :param cmd:
        :return:
        """
        try:
            self.lock.acquire()
            numbefore = self.stdinreader.get_num_of_lines()
            self.stdoutwriter.addCommand(cmd)
            numnow = self.stdinreader.get_num_of_lines()
            tries = 0
            while (numnow <= numbefore):
                numnow = len(self.stdinreader.get_lines())
                if (tries > self.maxtries):
                    raise Exception("Exabgp did not answer!")
                tries += 1
                time.sleep(self.sleeptime)
            out = self.stdinreader.get_current_line()
        finally:
            self.lock.release()
        return out

