#!/usr/bin/env python
import settings
from os.path import abspath, dirname

PROJECT_ROOT = abspath(dirname(__file__))

activate_this = PROJECT_ROOT + "/../vtenv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from socketio.server import SocketIOServer
from push import handle

from logger import Logger

if __name__ == "__main__":
    transports = settings.TRANSPORTS
    
    if settings.PRODUCTION_MODE:
        Logger().log.info("Serving on https://%s:%s'" % (settings.HOST, settings.PORT))
        SocketIOServer((settings.HOST, settings.PORT), handle, transports=transports, policy_server=False, keyfile=settings.KEY_FILE, certfile=settings.CERT_FILE).serve_forever()
    else:
        Logger().log.info("Serving on http://%s:%s'" % (settings.HOST, settings.PORT))
        SocketIOServer((settings.HOST, settings.PORT), handle, transports=transports, policy_server=False).serve_forever()