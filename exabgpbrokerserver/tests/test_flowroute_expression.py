__author__ = 'markus'
from unittest import TestCase

import exabgpbrokerserver.exabgpmods.flowroute.expressions


class FlowRouteExpressionTest(TestCase):

    def test_port_expressions(self):
        exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("9000")
        exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("=80&=50")
        exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("=80&=50&=80&=90")
        exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("<80&>90&<80&<90&<80&<100")
        exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("<80&>90&<80&<90&<80&<100&>90&<80&>90&<80&>90&<80&>90&<80")

    def test_invalid_port_expressions(self):
        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("-80")

        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("=80&")

        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("<80&>90000")

        with self.assertRaises(ValueError):
            exabgpbrokerserver.exabgpmods.flowroute.expressions.PortExpression("-9000")

