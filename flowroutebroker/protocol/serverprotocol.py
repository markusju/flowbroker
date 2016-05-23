__author__ = 'markus'


import socket
import replies
import requestanalyzer
from exceptions import EvaluationError


class ServerProtocol:

    def __init__(self, sock, sockfile):
        self.sock = sock  # type: socket.socket
        self.sockfile = sockfile  # type: socket._fileobject
        self.currentLine = None

    def run(self):
            try:
                request = requestanalyzer.RequestAnalyzer(self)
                print request.request_method
                print request.request_method_args
                print request.parameters

            except socket.error as sockerr:
                if "timed out" in sockerr.message:
                    self.put_line(replies.Reply408().to_str())
                else:
                    self.put_line(replies.Reply500().to_str())

            except IOError:
                # Client disconnected
                pass

            except EvaluationError:
                self.put_line(replies.Reply400().to_str())

            except Exception:
                self.put_line(replies.Reply500().to_str())

    def get_current_line(self):
        return self.currentLine

    def readline(self):
        line = self.sockfile.readline()
        # Remove Newline from Content
        if not line:
            raise IOError("No more data")
        self.currentLine = line

    def put_line(self, line):
        self.sock.sendall(line+"\n")

