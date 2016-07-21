#!/usr/bin/python
__author__ = 'markus'

import time

from exabgpbrokerserver import exabgp
import flowroutebroker
from exabgpbrokerserver.flowroutebroker.config import ConfigError


def main():
    try:

        api = exabgp.getApi()

        server = flowroutebroker.Server(api)
        server.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                server.stop_server()
                break

    except ConfigError as e:
        print "You have an error in your configuration file, exiting."
        print e.message

    except Exception as e:
        print "An error occured, exiting."
        print e.message

    finally:
        exit()


if __name__ == "__main__":
    main()
