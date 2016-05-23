__author__ = 'markus'

from processinterface import ProcessInterface
from stdinreader import StdInReader
from stdoutwriter import StdOutWriter
from api import Api
from flowroute import FlowRoute

def getApi():
    """
    Returns an instance of the API
    :return:
    """
    iface = ProcessInterface()
    reader = StdInReader(iface)
    reader.start()

    writer = StdOutWriter(iface)
    writer.start()

    api = Api(reader, writer)
    return api