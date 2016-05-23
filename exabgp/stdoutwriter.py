__author__ = 'markus'


import threading


class StdOutWriter (threading.Thread):

    def __init__(self, processinterface):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.cmdQueue = []
        self.sema = threading.Semaphore(0)
        self.processinterface = processinterface

    def run(self):
        while True:
            self.sema.acquire()
            command = self.cmdQueue.pop(0)
            self.processinterface.send_command(command)

    def addCommand(self, command):
        """
        Adds a new command to queue
        :param command:
        :return:
        """
        self.cmdQueue.append(command)
        self.sema.release()

