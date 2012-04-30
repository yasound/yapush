#!/usr/bin/env python
import sys

import os
from os.path import abspath, dirname, join
HOST = '0.0.0.0'
PORT = 9000

PROJECT_ROOT = abspath(dirname(__file__))

# Uncomment this if you use Virtualenv
#
activate_this = PROJECT_ROOT + "/../vtenv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from socketio.server import SocketIOServer
from push import handle

if __name__ == "__main__":
    print "Serving on http://%s:%s'" % (HOST, PORT)
    SocketIOServer((HOST, PORT), handle, policy_server=False).serve_forever()
