__author__ = 'markus'

import threading


class StdInReader (threading.Thread):

    def __init__(self, processinterface):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sema = threading.Semaphore(0)
        self.processinterface = processinterface
        self.lines = []

    def run(self):
        while True:
            out = self.processinterface.read_line()
            self.lines.append(out)

    def getLines(self):
        """
        Gets all lines written to STDINT
        :return:
        """
        return self.lines

    def getNumOfLines(self):
        """
        Gets the Num of lines written to STDIN
        :return:
        """
        return len(self.lines)

    def getCurrentLine(self):
        """
        Gets the last line written to STDIN
        :return:
        """
        if (len(self.lines) < 1):
            return None
        return self.lines[-1]
