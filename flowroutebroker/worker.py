__author__ = 'markus'

import threading
import socket
import protocol
import protocol.replies

from exabgp import FlowRoute


class Worker (threading.Thread):

    def __init__(self, sock, addr, api):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sock = sock # type: socket.socket
        self.sock.settimeout(10)
        self.sockfile = self.sock.makefile()
        self.addr = addr
        self.api = api

    def run(self):
        """
        Starts a worker process and instantiates a new Protocol session
        :return:
        """
        try:
            protocol.ServerProtocol(self.sock, self.sockfile, self.addr, self.api).run()
        finally:
            self.sockfile.close()
            self.sock.close()

    def stop_worker(self):
        self.sockfile.close()
        self.sock.close()
