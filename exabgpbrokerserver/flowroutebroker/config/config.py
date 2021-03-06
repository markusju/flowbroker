__author__ = 'markus'

import yaml

from exabgpbrokerserver.exabgpmods.flowroute.flowroute import ip_cidr_pattern
from configexception import ConfigError


class Config:
    def __init__(self, filename="config.yml"):

        # Paths to look for the file
        paths = ["", "/etc/broker-server/", "/etc/exabgp/broker-server/"]

        ymlfile = None
        count = 0

        for path in paths:
            try:
                ymlfile = open(path+filename, 'r')
                break
            except IOError as err:
                count += 1
                if count >= len(paths):
                    raise Exception("Cound not find a valid config file!")
                continue

        self.cfg = yaml.safe_load(ymlfile)
        self._pre_checks()
        self._semantic_checks()

    def _pre_checks(self):
        """
        Syntactical Analysis
        :return:
        """

        if not self.cfg:
            raise ConfigError("Your config file seems to be empty");

        if "broker" not in self.cfg :
            raise ConfigError("You must define 'broker'")

        if "bind-address" not in self.cfg["broker"]:
            self.cfg["broker"]["bind-address"] = "0.0.0.0"

        if "port" not in self.cfg["broker"]:
            self.cfg["broker"]["port"] = 5653

        if "tolerance" not in self.cfg["broker"]:
            raise ConfigError("You must define 'tolerance' in the 'broker' context")

        if "hosts" not in self.cfg:
            raise ConfigError("You must define 'hosts'")

        if not self.cfg["hosts"] or "default" not in self.cfg["hosts"]:
            raise ConfigError("You must define 'default' in the 'hosts' context")

        if not self.cfg["hosts"]["default"] or "secret" not in self.cfg["hosts"]["default"]:
            raise ConfigError("You must define 'secret' in the 'default' context contained in the 'hosts' context")

    def _semantic_checks(self):
        """
        Semantic Analysis
        :return:
        """

        if not ip_cidr_pattern.match(self.cfg["broker"]["bind-address"]+"/32"):
            raise ConfigError("Invalid Bind Address")

        if self.cfg["broker"]["port"] not in range(0, 65535):
            raise ConfigError("Invalid Listen Port")

        for ip in self.cfg["hosts"]:

            if not ip_cidr_pattern.match(ip+"/32") and ip != "default":
                raise ConfigError("You have defined an invalid IP address '" + ip + "' in the 'hosts' context")

            if not self.cfg["hosts"][ip]:
                raise ConfigError("You haved defined the host '"+ ip +"' but did not provide any configuration parameters in its context. Tryn' to be funny, huh? Not cool, dude.")

            if "subnets" in self.cfg["hosts"][ip]:
                for subnetips in self.cfg["hosts"][ip]["subnets"]:
                    if not ip_cidr_pattern.match(subnetips):
                        raise ConfigError("You have defined an invalid IP address '"+ subnetips +"' in the 'subnets' context for the host '" + ip + "'")

    def get_tolerance(self):
        return long(self.cfg["broker"]["tolerance"])

    def get_bind_address(self):
        return self.cfg["broker"]["bind-address"]

    def get_listen_port(self):
        return int(self.cfg["broker"]["port"])

    def get_secret_for_host(self, ip):
        if ip in self.cfg["hosts"]:
            return self.cfg["hosts"][ip]["secret"]
        return self.cfg["hosts"]["default"]["secret"]

    def is_destination_permitted(self, ip, destination):
        # Requesting IP is always permitted
        if ip+"/32" == destination:
            return True

        # Check if there is a config entry for the requesting host...
        if ip in self.cfg["hosts"]:
            for net in self.cfg["hosts"][ip]["subnets"]:
                if self.__address_in_network(destination, net):
                    return True

        return False

    def __ip_to_int(self, ip):
        """
        Converts an IP address to its long representation
        :param ip:
        :return:
        """
        o = map(int, ip.split('.'))
        res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
        return res

    def __is_cidr_in_cidr(self, ip_a, mask_a, ip_b, mask_b):
        """
        Checks whether Net A is contained or equal in/to Net B
        Adapted from: http://stackoverflow.com/questions/819355/how-can-i-check-if-an-ip-is-in-a-network-in-python
        :param ip_a:
        :param mask_a:
        :param ip_b:
        :param mask_b:
        :return:
        """

        mask_a = int(mask_a)
        mask_b = int(mask_b)

        maskLengthFromRight_a = 32 - mask_a
        maskLengthFromRight_b = 32 - mask_b

        ipNetworkInt_a = self.__ip_to_int(ip_a) # convert the ip network into integer form
        ipNetworkInt_b = self.__ip_to_int(ip_b) # convert the ip network into integer form

        binString_a = "{0:b}".format(ipNetworkInt_a) # convert that into into binary (string format)
        binString_b = "{0:b}".format(ipNetworkInt_b) # convert that into into binary (string format)

        chopAmount_a = 0 # find out how much of that int I need to cut off
        chopAmount_b = 0 # find out how much of that int I need to cut off

        for i in range(maskLengthFromRight_a):
            if i < len(binString_a):
                chopAmount_a += int(binString_a[len(binString_a)-1-i]) * 2**i

        for i in range(maskLengthFromRight_b):
            if i < len(binString_b):
                chopAmount_b += int(binString_b[len(binString_b)-1-i]) * 2**i


        minVal_a = ipNetworkInt_a-chopAmount_a
        maxVal_a = minVal_a+2**maskLengthFromRight_a -1

        minVal_b = ipNetworkInt_b-chopAmount_b
        maxVal_b = minVal_b+2**maskLengthFromRight_b -1

        return minVal_a >= minVal_b and maxVal_a <= maxVal_b

    def __address_in_network(self, check_net, target_net):
        netaddr_check, bits_check = check_net.split('/')
        netaddr_target,bits_target = target_net.split('/')
        return self.__is_cidr_in_cidr(netaddr_check, bits_check, netaddr_target, bits_target)
