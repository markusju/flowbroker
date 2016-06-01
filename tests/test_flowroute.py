from unittest import TestCase

import flowroutebroker
import exabgp

__author__ = 'markus'


class FlowRouteTest(TestCase):

    def setUp(self):
        self.flowroute = exabgp.FlowRoute()

    def test_no_action(self):
        try:
            self.flowroute.build_route()
        except Exception:
            return
        self.fail("No Exception thrown for unspecified action")

    def test_invalid_ip_cidr(self):
        with self.assertRaises(ValueError):
            self.flowroute.source_address = "8.8.8.8/33"

        with self.assertRaises(ValueError):
            self.flowroute.source_address = "256.24.23.1/24"

        with self.assertRaises(ValueError):
            self.flowroute.source_address = "aa.vv.aa.ss/12"

        with self.assertRaises(ValueError):
            self.flowroute.source_address = "12.12.12.-1/12"

    def test_source(self):
        self.flowroute.source_address = "8.8.8.8/32"
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { source 8.8.8.8/32; } then { discard; } }")

    def test_destination(self):
        self.flowroute.destination_address = "123.0.0.1/14"
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { destination 123.0.0.1/14; } then { discard; } }")

    def test_port(self):
        self.flowroute.source_port = ["=80", ">80&<90"]
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { source-port [ =80 >80&<90 ]; } then { discard; } }")

    def test_source_port(self):
        self.flowroute.port = ["=100", ">80&<90"]
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { port [ =100 >80&<90 ]; } then { discard; } }")

    def test_destination_port(self):
        self.flowroute.destination_port = ["=100", ">80&<90"]
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { destination-port [ =100 >80&<90 ]; } then { discard; } }")

    def test_invalid_destination_port(self):
        with self.assertRaises(ValueError):
            self.flowroute.destination_port = "=70000"

        with self.assertRaises(ValueError):
            self.flowroute.destination_port = "4000"

        with self.assertRaises(ValueError):
            self.flowroute.destination_port = "40&60"

        with self.assertRaises(ValueError):
            self.flowroute.destination_port = ">40&>213"

        with self.assertRaises(ValueError):
            self.flowroute.destination_port = ">40&<90000"

    def test_invalid_source_port(self):
        with self.assertRaises(ValueError):
            self.flowroute.source_port = "=70000"

        with self.assertRaises(ValueError):
            self.flowroute.source_port = "4000"

        with self.assertRaises(ValueError):
            self.flowroute.source_port = "40&60"

        with self.assertRaises(ValueError):
            self.flowroute.source_port = ">40&>213"

        with self.assertRaises(ValueError):
            self.flowroute.source_port = ">40&<90000"

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            self.flowroute.port = "=70000"

        with self.assertRaises(ValueError):
            self.flowroute.port = "4000"

        with self.assertRaises(ValueError):
            self.flowroute.port = "40&60"

        with self.assertRaises(ValueError):
            self.flowroute.port = ">40&>213"

        with self.assertRaises(ValueError):
            self.flowroute.port = ">40&<90000"

    def test_invalid_protocol(self):
        with self.assertRaises(ValueError):
            self.flowroute.protocol = "teaseepee"

    def test_protocol(self):
        self.flowroute.protocol = "udp"
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { protocol udp; } then { discard; } }")

        self.flowroute.protocol = "tcp"
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { protocol tcp; } then { discard; } }")

        self.flowroute.protocol = ["tcp", "udp"]
        self.flowroute.filter_action = "discard"
        self.assertEquals(str(self.flowroute), "flow route  { match { protocol [ tcp udp ]; } then { discard; } }")



