__author__ = 'markus'

import socket
import worker
import threading


class Server (threading.Thread):

    def __init__(self, api):
        threading.Thread.__init__(self)
        self.api = api
        self.workers = []
        self.interrupt = threading.Event()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Avoid Address already in use errors
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Set socket timeout to 1 second
        self.socket.settimeout(1)

    def run(self):
        self.socket.bind(("0.0.0.0", 5653))
        #Backlog = 0
        self.socket.listen(5)
        #Ensure clean shutdown
        while not self.interrupt.isSet():
                try:
                    #Accept socket with 1 second timeout
                    sock, addr = self.socket.accept()
                    #Newly created sockets should not have a timeout by default
                    sock.settimeout(None)
                    work = worker.Worker(sock, addr, self.api)
                    self.workers.append(work)
                    work.start()
                except socket.error as exc:
                    if "timed out" in exc.message:
                        pass
                    else:
                        raise exc

    def stop_server(self):
        self.interrupt.set()
        self.socket.close()

        for worker_threads in self.workers:
            worker_threads.stop_worker()

