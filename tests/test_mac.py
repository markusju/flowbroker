from unittest import TestCase

from flowroutebroker import security

__author__ = 'markus'


class MacTest(TestCase):

    def setUp(self):
        self.mac = security.MessageAuthenticationCode("apr95glpdq48fhcm3qiu32kcxklo6134yaasplgjf953mklg")

    def test_sign(self):
        signature = self.mac.get_mac_for_message("test-message")
        self.assertEquals(signature, "efeaf7793ed9e17270f348387d60106a8900ecc975e365953990daa2c3897b30")

    def test_verify(self):
        self.mac.check_mac_for_message("efeaf7793ed9e17270f348387d60106a8900ecc975e365953990daa2c3897b30", "test-message")
