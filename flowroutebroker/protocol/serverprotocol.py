__author__ = 'markus'


import socket
import replies
import requestanalyzer
import commands
from exceptions import EvaluationError



class ServerProtocol:

    def __init__(self, sock, sockfile):
        self.sock = sock  # type: socket.socket
        self.sockfile = sockfile  # type: socket._fileobject
        self.currentLine = None

    def run(self):
            try:
                request = requestanalyzer.RequestAnalyzer(self)
                cmdeval = commands.CommandEvaluator(request)

                server_reply = cmdeval.get_command().execute("asd")
                self.put_line(server_reply)

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

            #except Exception:
                #self.put_line(replies.Reply500().to_str())

    def get_current_line(self):
        return self.currentLine

    def readline(self):
        line = self.sockfile.readline()
        # Remove Newline from Content
        if not line:
            raise IOError("No more data")
        self.currentLine = line

    def put_line(self, line):
        if not isinstance(line, str):
            raise ValueError("Only Strings are supported for put_line")
        self.sock.sendall(line+"\n")

