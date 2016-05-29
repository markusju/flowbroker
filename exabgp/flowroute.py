__author__ = 'markus'

import re
import inspect

class FlowRoute(object):
    """
    Representation of EXABGP's flow route syntax
    """

    def __init__(self):
        self._ip_pattern = re.compile(
            "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
            "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
            "(\/([0-9]|[1-2][0-9]|3[0-2]))$")

        self._action_pattern = re.compile("^(discard|rate-limit [0-9]+)$")

        self._name = ""
        self._source_address = ""
        self._destination_address = ""
        self._protocol = ""
        self._port = ""
        self._source_port = ""
        self._destination_port = ""
        self._filter_action = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def destination_address(self):
        return self._destination_address

    @destination_address.setter
    def destination_address(self, value):
        self._check_valid_ip_cidr(value)
        self._destination_address = value

    @property
    def source_address(self):
        return self._source_address

    @source_address.setter
    def source_address(self, value):
        self._check_valid_ip_cidr(value)
        self._source_address = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        if value not in ["tcp", "udp"]:
            raise ValueError("Invalid protocol")
        self._protocol = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def filter_action(self):
        return self._filter_action

    @filter_action.setter
    def filter_action(self, value):
        self._check_valid_action(value)
        self._filter_action = value

    @property
    def destination_port(self):
        return self._destination_port

    @destination_port.setter
    def destination_port(self, value):
        self._destination_port = value

    @property
    def source_port(self):
        return self._source_port

    @source_port.setter
    def source_port(self, value):
        self._source_port = value

    def _is_valid_action(self, value):
        return self._action_pattern.match(value)

    def _check_valid_action(self, value):
        if not self._is_valid_action(value):
            raise ValueError("Invalid Action specified")

    def _is_valid_ip_cidr(self, value):
        """
        Returns whether the given IP/CIDR is valid
        :param value:
        :return:
        """
        return self._ip_pattern.match(value)

    def _check_valid_ip_cidr(self, value):
        """
        Checks whether the supplied IP/CIDR is valid. Raises an exception if not
        :param value:
        :return:
        """
        if not self._is_valid_ip_cidr(value):
            raise ValueError("Invalid IP/CIDR")

    def count_match_criteria(self):
        match_crit = [self.protocol, self.destination_address, self.source_address, self.port, self.source_port, self.destination_port]
        count_match_crit = 0

        for crit in match_crit:
            if crit != "":
                count_match_crit += 1
        return count_match_crit

    def is_filter_action_set(self):
        return self.filter_action is not False

    def build_route(self):
        if not self.is_filter_action_set():
            raise Exception("No FilterAction specified. Cannot build route")

        if self.count_match_criteria() < 1:
            raise Exception("No Match Criteria specified. Cannot build route")

        flow_route = []

        flow_route.append("flow route " + self.name + " { ")

        flow_route.append("match { ")

        if self.source_address:
            flow_route.append("source ")
            flow_route.append(self.source_address)
            flow_route.append("; ")

        if self.destination_address:
            flow_route.append("destination ")
            flow_route.append(self.destination_address)
            flow_route.append("; ")

        if self.source_port:
            flow_route.append("source-port ")
            flow_route.append(self.source_port)
            flow_route.append("; ")

        if self.destination_port:
            flow_route.append("destination-port ")
            flow_route.append(self.destination_port)
            flow_route.append("; ")

        if self.protocol:
            flow_route.append("protocol ")
            flow_route.append(self.protocol)
            flow_route.append("; ")

        flow_route.append("} ")

        flow_route.append("then { ")
        flow_route.append(self.filter_action)
        flow_route.append("; ")
        flow_route.append("} ")

        flow_route.append("}")

        return str.join("", flow_route)

    def __str__(self):
        return self.build_route()