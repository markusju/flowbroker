__author__ = 'markus'

import threading


class StdInReader (threading.Thread):
    """
    Enables async Reading from STDIN
    """

    def __init__(self, processinterface):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sema = threading.Semaphore(0)
        self.processinterface = processinterface
        self.lines = []

    def run(self):
        """
        Thread Loop for Reading
        :return:
        """
        while True:
            # Blocking Read
            out = self.processinterface.read_line()
            self.lines.append(out)

    def get_lines(self):
        """
        Gets all lines written to STDINT
        :return:
        """
        return self.lines

    def get_num_of_lines(self):
        """
        Gets the Num of lines written to STDIN
        :return:
        """
        return len(self.lines)

    def get_current_line(self):
        """
        Gets the last line written to STDIN
        :return:
        """
        if len(self.lines) < 1:
            return None
        return self.lines[-1]
