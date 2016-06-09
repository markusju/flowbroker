__author__ = 'markus'

from numberrange import NumberRange


class PortExpression(NumberRange):

    @staticmethod
    def __is_valid_port(port):
        return 0 < int(port) <= 65535

    @staticmethod
    def __is_valid_prefix(prefix):
        return prefix in ["<", ">", "="]

    def _check_prefix(self, prefix):
        if not self.__is_valid_prefix(prefix):
            raise ValueError("Invalid Prefix!")

    def _check_port(self, port):
        if not self.__is_valid_port(port):
            raise ValueError("Invalid Port!")

    def analyze_element(self, element):
        """
        Performs analysis per element
        :param element:
        :return:
        """
        if not element:
            raise ValueError("No Sub-Expression after ampersand operator")

        if element.isdigit():
            if self.get_num_of_elements() == 1:
                self._check_port(element)
                return
            else:
                raise ValueError("Missing Prefix")

        prefix = element[0]
        self._check_prefix(prefix)
        self._check_port(element[1:])





