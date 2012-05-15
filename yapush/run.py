#!/usr/bin/env python
import sys

import os
from os.path import abspath, dirname, join

HOST = '0.0.0.0'
PORT = 9000
CERT_FILE = '/etc/nginx/ssl/server.crt'
KEY_FILE = '/etc/nginx/ssl/server.key'

PROJECT_ROOT = abspath(dirname(__file__))

# Uncomment this if you use Virtualenv
#
activate_this = PROJECT_ROOT + "/../vtenv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from socketio.server import SocketIOServer
from push import handle

APP_MODE = os.environ.get('DJANGO_MODE', False)
PRODUCTION_MODE = ( APP_MODE == 'production' )
DEVELOPMENT_MODE = ( APP_MODE == 'development' )
LOCAL_MODE = not ( PRODUCTION_MODE or DEVELOPMENT_MODE )

if __name__ == "__main__":
    if PRODUCTION_MODE:
        print "Serving on https://%s:%s'" % (HOST, PORT)
        SocketIOServer((HOST, PORT), handle, policy_server=False, keyfile=KEY_FILE, certfile=CERT_FILE).serve_forever()
    else:
        print "Serving on http://%s:%s'" % (HOST, PORT)
        SocketIOServer((HOST, PORT), handle, policy_server=False).serve_forever()