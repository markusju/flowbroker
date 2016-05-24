__author__ = 'markus'

from DISCARD import DISCARD
from RATELIMIT import RATELIMIT
from UNSUPPORTED import UNSUPPORTED
from abstractcommand import AbstractCommand

from flowroutebroker.protocol.requestanalyzer import RequestAnalyzer


class CommandFactory:
    """
    Provides Instances of Commands
    """

    def __init__(self, requestanalyzer):
        if not isinstance(requestanalyzer, RequestAnalyzer):
            raise ValueError("Argument must be instance of RequestAnalyzer")
        self.requestanalyzer = requestanalyzer

        # Command dict containing all commands
        self.cmdmap = {
            "DISCARD": lambda x: DISCARD(x),
            "RATELIMIT": lambda x: RATELIMIT(x),
            "UNSUPPORTED": lambda x: UNSUPPORTED(x)
        }

    def get_command(self):
        """
        Returns an instance of the command
        :return AbstractCommand:
        """
        method = self.requestanalyzer.request_method

        # Command not found
        if method not in self.cmdmap:
            return self.cmdmap["UNSUPPORTED"](self.requestanalyzer)

        cmd = self.cmdmap[method](self.requestanalyzer)

        if not isinstance(cmd, AbstractCommand):
            raise RuntimeError("Illegal Command Type")

        return cmd

