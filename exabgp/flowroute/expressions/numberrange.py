__author__ = 'markus'

from abc import ABCMeta, abstractmethod


class NumberRange:
        __metaclass__ = ABCMeta

        def __init__(self):
            self.__inputstr = ""
            self.__splitstr = []

        def analyze(self, inputstr):
            """
            Start analyzing a input string
            :param inputstr:
            :return:
            """
            self.__inputstr = str(inputstr)
            self.__splitstr = str.split(self.__inputstr, "&")

            if not self.__inputstr:
                raise ValueError("Not a valid NumberRange Expression")

            if not self.__splitstr:
                self.analyze_element(self.__inputstr)

            for el in self.__splitstr:
                self.analyze_element(el)

        def get_num_of_elements(self):
            return len(self.__splitstr)

        @abstractmethod
        def analyze_element(self, element):
            """
            Analyzes each element of the given range expression
            :param element:
            :return:
            """
            pass

        def __str__(self):
            return self.__inputstr

