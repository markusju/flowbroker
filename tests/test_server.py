from unittest import TestCase

import flowroutebroker

__author__ = 'markus'


class TestServer(TestCase):

    def __init__(self):
        self.server = flowroutebroker.Server()

    def test_start(self):
      self.server.start()


