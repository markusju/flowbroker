__author__ = 'markus'

import re
from expressions import PortExpression, NumberRange, PacketLengthExpression, DSCPExpression


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

        self._flow_name = ""
        self._flow_source_address = ""
        self._flow_destination_address = ""
        self._flow_protocol = ""
        self._flow_port = ""
        self._flow_source_port = ""
        self._flow_destination_port = ""
        self._flow_icmp_type = ""
        self._flow_icmp_code = ""
        self._flow_tcp_flags = ""
        self._flow_packet_length = ""
        self._flow_fragment = ""
        self._flow_dscp = ""
        self._flow_filter_action = ""

    @property
    def name(self):
        return self._flow_name

    @name.setter
    def name(self, value):
        self._flow_name = value

    @property
    def destination_address(self):
        return self._flow_destination_address

    @destination_address.setter
    def destination_address(self, value):
        self._check_valid_ip_cidr(value)
        self._flow_destination_address = value

    @property
    def source_address(self):
        return self._flow_source_address

    @source_address.setter
    def source_address(self, value):
        self._check_valid_ip_cidr(value)
        self._flow_source_address = value

    @property
    def protocol(self):
        return self._flow_protocol

    @protocol.setter
    def protocol(self, value):
        allowed_prot = ["tcp", "udp"]
        self._flow_protocol = self._check_allowed_values(allowed_prot, value)

    @property
    def port(self):
        return self._flow_port

    @port.setter
    def port(self, value):
        self._flow_port = self._check_allowed_values_numberrange(PortExpression(), value)

    @property
    def filter_action(self):
        return self._flow_filter_action

    @filter_action.setter
    def filter_action(self, value):
        self._check_valid_action(value)
        self._flow_filter_action = value

    @property
    def destination_port(self):
        return self._flow_destination_port

    @destination_port.setter
    def destination_port(self, value):
        self._flow_destination_port = self._check_allowed_values_numberrange(PortExpression(), value)

    @property
    def source_port(self):
        return self._flow_source_port

    @source_port.setter
    def source_port(self, value):
        self._flow_source_port = self._check_allowed_values_numberrange(PortExpression(), value)

    @property
    def icmp_type(self):
        return self._flow_icmp_type

    @icmp_type.setter
    def icmp_type(self, value):
        self._flow_icmp_type = self._check_allowed_values(
            ["echo-reply", "echo-request", "info-reply", "info-request", "mask-reply",
             "mask-request", "parameter-problem", "redirect", "router-advertisement",
             "router-solicit", "source-quench", "time-exceeded", "timestamp", "timestamp-reply",
             "unreachable"],
            value
        )

    @property
    def icmp_code(self):
        return self._flow_icmp_code

    @icmp_code.setter
    def icmp_code(self, value):
        self._flow_icmp_code = self._check_allowed_values(
            ["communication-prohibited-by-filtering", "destination-host-prohibited ", "destination-host-unknown ",
             "destination-network-unknown ", "fragmentation-needed ", "host-precedence-violation",
             "ip-header-bad", "network-unreachable", "network-unreachable-for-tos ",
             "port-unreachable", "redirect-for-host","redirect-for-network",
             "redirect-for-tos-and-host", "redirect-for-tos-and-net", "required-option-missing",
             "source-host-isolated", "source-route-failed", "ttl-eq-zero-during-reassembly",
             "ttl-eq-zero-during-transit"],
            value
        )

    @property
    def tcp_flags(self):
        return self._flow_tcp_flags

    @tcp_flags.setter
    def tcp_flags(self, value):
        self._flow_tcp_flags = self._check_allowed_values(
            ["fin", "syn", "rst", "push", "ack", "urgent"],
            value
        )

    @property
    def packet_length(self):
        return self._flow_packet_length

    @packet_length.setter
    def packet_length(self, value):
        self._flow_packet_length = self._check_allowed_values_numberrange(PacketLengthExpression(), value)

    @property
    def dscp(self):
        return self._flow_dscp

    @dscp.setter
    def dscp(self, value):
        # TODO: checks
        self._flow_dscp = self._check_allowed_values_numberrange(DSCPExpression(), value)

    @property
    def fragment(self):
        # TODO: Checks
        return self._flow_fragment

    @fragment.setter
    def fragment(self, value):
        self._flow_fragment = self._check_allowed_values(["not-a-fragment", "dont-fragment",
                                                          "is-fragment", "first-fragment",
                                                          "last-fragment"],
                                                         value)

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

    def _check_allowed_values(self, allowed_vals, input_val):
        """
        Checks whether a given input list validates against a given list of valid expressions.
        This method accepts Lists and String and returns an EXABGP compatible String representation
        :param allowed_vals:
        :param input_val:
        :return:
        """
        if type(input_val) is not list and input_val not in allowed_vals:
            raise ValueError("Invalid Value")

        # Check if supplied var is list and whether it is a subset of the allowed arguments
        if type(input_val) is list and not (set(input_val) <= set(allowed_vals)) or bool(input_val) is False:
            raise ValueError("Invalid Value")

        return self._format_expression_list(input_val)

    def _check_allowed_values_numberrange(self, number_range, input_val):

        if not isinstance(number_range, NumberRange):
            raise ValueError("number_range must be of type NumberRange")

        if type(input_val) is not list:
            number_range.analyze(input_val)

        if type(input_val) is list:
            for el in input_val:
                number_range.analyze(el)

        return self._format_expression_list(input_val)

    def _check_allowed_values_regexp(self, regex, input_val):
        """
        Checks whether a given input validates against a given Regexp.
        This method accepts Lists and Strings and returns a EXABGP compatible String representation
        :param regex:
        :param input_val:
        :return:
        """
        #if not isinstance(regex, re.__Regex):
            #raise ValueError("regex must be of type __Regex")

        if type(input_val) is not list and not regex.match(input_val):
            raise ValueError("Invalid Value")

        if type(input_val) is list:
            for el in input_val:
                if not regex.match(el):
                    raise ValueError("Invalid Expression")

        return self._format_expression_list(input_val)

    def _format_expression_list(self, input_val):
        """
        Formats the Input according to EXABGP's requirements.
        This method takes a string or a list.
        Lists with one element are converted to a string.
        :param input_val:
        :return:
        """
        if isinstance(input_val, list):
            # If list only contains one value..
            if len(input_val) == 1:
                return input_val[0]
            output_buff = ["["]
            for el in input_val:
                output_buff.append(" ")
                output_buff.append(el)
            output_buff.append(" ]")
            return str.join("", output_buff)
        return str(input_val)


    def count_match_criteria(self):
        """
        Returns the number of set match criteria
        :return:
        """
        match_crit = [self.protocol, self.destination_address, self.source_address,
                      self.port, self.source_port, self.destination_port, self.icmp_code,
                      self.icmp_type, self.tcp_flags, self.fragment, self.packet_length,
                      self.dscp]

        count_match_crit = 0
        for crit in match_crit:
            if crit != "":
                count_match_crit += 1
        return count_match_crit

    def is_filter_action_set(self):
        return bool(self.filter_action) is not False


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

        if self.port:
            flow_route.append("port ")
            flow_route.append(self.port)
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

        if self.icmp_code:
            flow_route.append("icmp-code ")
            flow_route.append(self.icmp_code)
            flow_route.append("; ")

        if self.tcp_flags:
            flow_route.append("tcp-flags ")
            flow_route.append(self.tcp_flags)
            flow_route.append("; ")

        if self.fragment:
            flow_route.append("fragment ")
            flow_route.append(self.fragment)
            flow_route.append("; ")

        if self.packet_length:
            flow_route.append("packet-length ")
            flow_route.append(self.packet_length)
            flow_route.append("; ")

        if self.dscp:
            flow_route.append("dscp ")
            flow_route.append(self.dscp)
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