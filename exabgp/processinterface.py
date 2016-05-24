__author__ = 'markus'


import sys


class ProcessInterface:
    """
    Interface to the EXABGP process
    """
    def send_command(self, command):
        """
        Sends a command to EXABGP
        :param command:
        :return:
        """
        sys.stdout.write(command + "\n")
        sys.stdout.flush()

    def read_line(self):
        """
        Reads a line from EXABGP
        :return:
        """
        return sys.stdin.readline()
