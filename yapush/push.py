from gevent import Greenlet, monkey, pywsgi, queue
from socketio import SocketIOServer, socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
import datetime
import gevent
import json
import redis
monkey.patch_all()

HOST = '0.0.0.0'
PORT = 9000

class RadioNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_subscribe(self, data):
        print "subscribe! : %s" % (data)
        
        radio_id = data['radio_id']
        
        self.spawn(self.listener, radio_id)
        
    def listener(self, radio_id):
        r = redis.StrictRedis()
        r = r.pubsub()
        
        channel = 'radio.%s' % (radio_id)
        r.subscribe(channel)

        for m in r.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                self.emit("wall_event", data)

def handle(environ, start_response):
    return socketio_manage(environ, {'/radio': RadioNamespace})

print "Serving on http://%s:%s'" % (HOST, PORT)
SocketIOServer((HOST, PORT), handle, policy_server=False).serve_forever()
