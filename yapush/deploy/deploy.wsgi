#!/usr/bin/python
#
# WSGI File for Django

# To use with apache2 server please read README file


import os, sys
my_location = os.path.abspath(os.path.split(__file__)[0])

# Insert Project path
PROJECT_PATH = os.path.join(my_location, '../')
sys.path.insert(0,PROJECT_PATH)

# Uncomment this if you use VirtualEnv
#
activate_this = PROJECT_PATH + "/../vtenv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

sys.path.append('/usr/lib/pymodules/python2.6')
sys.path.append('/usr/lib/python2.6/dist-packages')

sys.stdout = sys.stderr

from push import RadioNamespace, handle
from socketio import socketio_manage
from gevent import monkey
monkey.patch_all()

def application(environ, start_response):
    return handle(environ, start_response)
