from gevent import Greenlet, monkey, pywsgi, queue
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
import datetime
import gevent
import json
import redis
monkey.patch_all()

import logging

FORMAT = '%(asctime)-15s %(message)s'
formatter = logging.Formatter(FORMAT)

log = logging.getLogger('MyLogger')
log.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


class RadioNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_subscribe(self, data):
        print "subscribe! : %s" % (data)
        
        radio_id = data['radio_id']
        self.spawn(self.listener, radio_id)
        
    def on_unsubscribe(self, data):
        self.kill_local_jobs()
        
    def listener(self, radio_id):
        r = redis.StrictRedis()
        r = r.pubsub()

        channel = 'radio.%s' % (radio_id)
        r.subscribe(channel)
        print "subscribing to %s" % (channel)
        for m in r.listen():
            print m
            self.emit('radio_event', m)

def handle(environ, start_response):
    return socketio_manage(environ, {'/radio': RadioNamespace})

