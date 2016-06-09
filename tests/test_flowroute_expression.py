__author__ = 'markus'
from unittest import TestCase

import flowroutebroker
import exabgp.flowroute.expressions


class FlowRouteExpressionTest(TestCase):

    def test_port_expressions(self):
        exabgp.flowroute.expressions.PortExpression("9000")
        exabgp.flowroute.expressions.PortExpression("=80&=50")
        exabgp.flowroute.expressions.PortExpression("=80&=50&=80&=90")
        exabgp.flowroute.expressions.PortExpression("<80&>90&<80&<90&<80&<100")
        exabgp.flowroute.expressions.PortExpression("<80&>90&<80&<90&<80&<100&>90&<80&>90&<80&>90&<80&>90&<80")

    def test_invalid_port_expressions(self):
        with self.assertRaises(ValueError):
            exabgp.flowroute.expressions.PortExpression("-80")

        with self.assertRaises(ValueError):
            exabgp.flowroute.expressions.PortExpression("=80&")

        with self.assertRaises(ValueError):
            exabgp.flowroute.expressions.PortExpression("<80&>90000")

        with self.assertRaises(ValueError):
            exabgp.flowroute.expressions.PortExpression("-9000")

