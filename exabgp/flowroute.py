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

        self.port_range_pattern = re.compile(
            "(^>([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
            "&<([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$)"
            "|(^=([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$)"
        )

        self._action_pattern = re.compile("^(discard|rate-limit [0-9]+)$")

        self._name = ""
        self._source_address = ""
        self._destination_address = ""
        self._protocol = ""
        self._port = ""
        self._source_port = ""
        self._destination_port = ""
        self._icmp_type = ""
        self._icmp_code = ""
        self._tcp_flags = ""
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
        allowed_prot = ["tcp", "udp"]
        self._protocol = self._check_allowed_values_str_and_list(allowed_prot, value)

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

    @property
    def icmp_type(self):
        return self._icmp_type

    @icmp_type.setter
    def icmp_type(self, value):
        self._icmp_type = self._check_allowed_values_str_and_list(
            ["echo-reply", "echo-request", "info-reply", "info-request", "mask-reply",
             "mask-request", "parameter-problem", "redirect", "router-advertisement",
             "router-solicit", "source-quench", "time-exceeded", "timestamp", "timestamp-reply",
             "unreachable"],
            value
        )

    @property
    def icmp_code(self):
        return self._icmp_code

    @icmp_code.setter
    def icmp_code(self, value):
        self._icmp_code = self._check_allowed_values_str_and_list(
            ["communication-prohibited-by-filtering", "destination-host-prohibited ", "destination-host-unknown ",
             "destination-network-unknown ", "fragmentation-needed ", "host-precedence-violation",
             "ip-header-bad", "network-unreachable","network-unreachable-for-tos ",
             "port-unreachable", "redirect-for-host","redirect-for-network",
             "redirect-for-tos-and-host", "redirect-for-tos-and-net", "required-option-missing",
             "source-host-isolated", "source-route-failed", "ttl-eq-zero-during-reassembly",
             "ttl-eq-zero-during-transit"],
            value
        )
    @property
    def tcp_flags(self):
        return self._tcp_flags

    @tcp_flags.setter
    def tcp_flags(self, value):
        self._tcp_flags = self._check_allowed_values_str_and_list(
            ["fin", "syn", "rst", "push", "ack", "urgent"],
            value
        )

    @property
    def packet_length(self):
        raise NotImplementedError()
        pass

    @packet_length.setter
    def packet_length(self, value):
        raise NotImplementedError()
        pass

    @property
    def dscp(self):
        raise NotImplementedError()
        pass

    @dscp.setter
    def dscp(self, value):
        raise NotImplementedError()
        pass

    @property
    def fragment(self):
        raise NotImplementedError()
        pass

    @fragment.setter
    def fragment(self, value):
        raise NotImplementedError()
        pass

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

    def _check_allowed_values_str_and_list(self, allowed_vals, input):
        if type(input) is not list and input not in allowed_vals:
            raise ValueError("Invalid Value")

        # Check if supplied var is list and whether it is a subset of the allowed arguments
        if type(input) is list and not (set(input) <= set(allowed_vals)) or bool(input) is False:
            raise ValueError("Invalid Value")

        if isinstance(input, list):
            # If list only contains one value..
            if len(input) == 1:
                return input[0]
            output_buff = ["["]
            for el in input:
                output_buff.append(" ")
                output_buff.append(el)
            output_buff.append(" ]")
            return str.join("", output_buff)

        return input

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

        if self.icmp_type:
            flow_route.append("icmp-type ")
            flow_route.append(self.icmp_type)
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