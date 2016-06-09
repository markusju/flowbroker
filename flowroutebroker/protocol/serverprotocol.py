__author__ = 'markus'


import socket
import replies
import requestanalyzer
import commands
import security
from exceptions import EvaluationError
from exceptions import SemanticError
from exceptions import PermError
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
        self.sechandler = security.MacHandler("secret")

    def run(self):
        """
        Processes a incoming Request and issues a reply to the client
        :return:
        """
        try:
            # Syntactical Analysis of the Request
            request = requestanalyzer.RequestAnalyzer(self)

            # Security Checks (Session Layer)
            # TODO:
            # self.sechandler.check_request(request)

            # Semantic Analsysis ot the request
            cmdeval = commands.CommandFactory(request)

            # Attempting to execute the command
            server_reply = cmdeval.get_command().execute(self.api)

            # Transmitting the Reply
            self.put_reply(server_reply)

        except socket.error as sockerr:
            if "timed out" in sockerr.message:
                self.put_reply(replies.Reply408())
            else:
                self.put_reply(replies.Reply500())

        except PermError:
            self.put_reply(replies.Reply403())

        except AuthError:
            self.put_reply(replies.Reply401())

        except EvaluationError:
            self.put_reply(replies.Reply400())

        except SemanticError:
            self.put_reply(replies.Reply422())

        except IOError:
            # Client disconnected
            pass
        # TODO:
        #except Exception as err:
            #self.put_line(replies.Reply500(err.message).to_str())

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

    def put_reply(self, reply, signed=True):
        """
        Sends a reply to the client
        :param reply:
        :return:
        """
        if not isinstance(reply, replies.AbstractReply):
            raise ValueError("Only AbstractReplies are supported for put_reply")
        # Apply Signatures
        if signed:
            self.sechandler.apply_to_reply(reply)
        self.put_line(reply.to_str())

    @property
    def get_addr(self):
        """
        Returns Address Tuple from socket
        (<IP>, <Port>)
        :return:
        """
        return self._addr
