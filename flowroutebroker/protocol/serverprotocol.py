__author__ = 'markus'


import socket
import replies
import requestanalyzer
import commands
from exceptions import EvaluationError
from exceptions import AuthError


class ServerProtocol (object):
    """
    Flow Route Broker Protocol Implementation
    """

    def __init__(self, sock, sockfile, addr, api):
        self.sock = sock  # type: socket.socket
        self.sockfile = sockfile  # type: socket._fileobject
        self.api = api
        self._addr = addr
        self.currentLine = None

    def run(self):
            try:
                request = requestanalyzer.RequestAnalyzer(self)
                cmdeval = commands.CommandFactory(request)

                server_reply = cmdeval.get_command().execute(self.api)
                self.put_line(server_reply)

            except socket.error as sockerr:
                if "timed out" in sockerr.message:
                    self.put_line(replies.Reply408().to_str())
                else:
                    self.put_line(replies.Reply500().to_str())

            except AuthError:
                self.put_line(replies.Reply403().to_str())

            except EvaluationError:
                self.put_line(replies.Reply400().to_str())

            except IOError:
                # Client disconnected
                pass

            #except Exception:
                #self.put_line(replies.Reply500().to_str())

    def get_current_line(self):
        """
        Returns the last line that was read
        :return:
        """
        return self.currentLine

    def readline(self):
        """
        Reads the next line
        Raises IOError when no more lines are available
        :return:
        """
        line = self.sockfile.readline()
        # Remove Newline from Content
        if not line:
            raise IOError("No more data")
        self.currentLine = line

    def put_line(self, line):
        """
        Puts a new line
        :param line:
        :return:
        """
        if not isinstance(line, str):
            raise ValueError("Only Strings are supported for put_line")
        self.sock.sendall(line+"\n")

    @property
    def get_addr(self):
        """
        Returns Address Tuple from socket
        (<IP>, <Port>)
        :return:
        """
        return self._addr
