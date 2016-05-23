__author__ = 'markus'


import sys


class ProcessInterface:

    def send_command(self, command):
        sys.stdout.write(command + "\n")
        sys.stdout.flush()

    def read_line(self):
        return sys.stdin.readline()
