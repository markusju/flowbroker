__author__ = 'markus'

from abc import ABCMeta, abstractmethod


class AbstractReply:
    __metaclass__ = ABCMeta

    def __init__(self, payload=None, parameters=None):

        # Clearing up default arguments
        if not payload:
            payload = ""

        if not parameters:
            parameters = {}

        # Checking Preconditions...
        if not isinstance(payload, basestring):
            raise ValueError("payload must be of type basetring")

        if not isinstance(parameters, dict):
            raise ValueError("parameters must be of type dict")

        for paramkey, paramvalue in parameters.items():
                if not isinstance(paramkey, basestring):
                    raise ValueError("ParameterKeys must all be of type basestring")

                if not isinstance(paramvalue, basestring):
                    raise ValueError("ParameterValues must all be of type basestring")

        # Assigning Values
        self.payload = payload
        self.parameters = parameters

    @abstractmethod
    def get_message(self):
        """
        Returns the message belonging to this reply
        :return:
        """
        pass

    @abstractmethod
    def get_code(self):
        """
        Returns the return code associated with this reply
        :return:
        """
        pass

    def get_paramters(self):
        """
        Returns a dict containing all parameters associated with this reply
        :return:
        """
        return self.parameters

    def get_payload(self):
        """
        Returns the payload associated with this reply
        :return:
        """
        return self.payload

    def to_str(self):
        """
        Returns a String Representation of the Reply
        :return:
        """
        output_buff = [str(self.get_code()) + " " + str(self.get_message())]

        # Are there Parameters in the dict?
        if self.get_paramters() is not False:
            for paramkey, paramvalue in self.parameters.items():
                output_buff.append("\n")
                output_buff.append(paramkey + ": " + paramvalue)

        # Is there a payload?
        if self.get_payload() is not False:
            output_buff.append("\n\n")
            output_buff.append(self.get_payload())



        return str.join("", output_buff)

    def __str__(self):
        return self.to_str()
