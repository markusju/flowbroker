__author__ = 'markus'
from unittest import TestCase

import exabgpbrokerserver.exabgp.flowroute.expressions


class FlowRouteExpressionTest(TestCase):

    def test_port_expressions(self):
        exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("9000")
        exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("=80&=50")
        exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("=80&=50&=80&=90")
        exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("<80&>90&<80&<90&<80&<100")
        exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("<80&>90&<80&<90&<80&<100&>90&<80&>90&<80&>90&<80&>90&<80")

    def test_invalid_port_expressions(self):
        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("-80")

        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("=80&")

        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("<80&>90000")

        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgp.flowroute.expressions.PortExpression("-9000")

