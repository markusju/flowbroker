__author__ = 'markus'

from exceptions import EvaluationError
from collections import OrderedDict

class RequestAnalyzer (object):

    def __init__(self, serverprotocol):
        """
        Startet eine syntaktische Analyse des Requests
        :param serverprotocol:
        :return:
        """
        self.serverprotocol = serverprotocol
        self.request_stack = []

        self._request_method = ""
        self._request_method_args = []

        self._parameters = OrderedDict()

        self.__analyze_request()
        self.__cleanup_request_stack()
        self.__evaluate_request()


    @property
    def client_port(self):
        return self.serverprotocol.get_addr[1]

    @property
    def client_ip(self):
        return self.serverprotocol.get_addr[0]

    @property
    def request_method(self):
        return self._request_method

    @property
    def request_method_args(self):
        return self._request_method_args

    @property
    def parameters(self):
        return self._parameters

    def __analyze_request(self):
        """
        Analyzes the incoming request from the client
        :return:
        """
        while True:
            try:
                self.serverprotocol.readline()
                self.request_stack.append(self.serverprotocol.get_current_line())
                
                # Abbruch-Bedingung fuer Lesevorgang (1x New line)
                if len(self.request_stack) > 1 and self.request_stack[-1] == "\n":
                    break

            # Solange lesen bis nichts mehr verfuegbar ist
            except IOError as exc:
                raise exc
            # Alle anderen durchreichen
            except Exception as exc:
                raise exc

    def __cleanup_request_stack(self):
        """
        Entfernt alle Eintraege die genau ein Newline-Zeichen sind und entfernt alle Newline-Zeichen, die sich am Ende eiens strings befinden.
        :return:
        """
        current_stack = self.request_stack
        new_stack = []

        for el in current_stack:
            if el[-1] == "\n" and len(el) > 1:
                new_stack.append(el[:-1])

        self.request_stack = new_stack

    def __evaluate_request(self):
        """
        Evaluates the previously recorded request
        :return:
        """
        if len(self.request_stack) < 1:
            raise EvaluationError()

        current_stack = self.request_stack

        method_parts = current_stack.pop(0).split(" ")
        self._request_method = method_parts.pop(0)
        self._request_method_args = method_parts

        for params in current_stack:
            #Split on first occurence
            parts = params.split(":", 1)

            # Parameters sind fehlerhaft
            if len(parts) != 2:
                raise EvaluationError()

            key = parts[0].strip()
            value = parts[1].strip()

            if not key or not value:
                raise EvaluationError()

            self.parameters[key] = value

    def to_string_for_signature_validation(self):
        out = []
        out.append(self.request_method)
        for el in self.request_method_args:
            out.append(" ")
            out.append(el)

        for key, value in self.parameters.iteritems():
            if key == "Signature": continue

            out.append("\n")
            out.append(key)
            out.append(": ")
            out.append(value)

        out.append("\n\n")

        return str.join("", out)
