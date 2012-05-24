from gevent import Greenlet, monkey, pywsgi, queue
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
import datetime
import gevent
import json
import redis
import settings
from logger import Logger

monkey.patch_all()


class RadioNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_subscribe(self, data):
        Logger().log.debug('receveid on_subscribe: %s' % (data))
        
        radio_id = data['radio_id']
        self.spawn(self.listener, radio_id)
        
    def on_unsubscribe(self, data):
        self.kill_local_jobs()
        
    def listener(self, radio_id):
        r = redis.StrictRedis(host=settings.REDIS_HOST, db=settings.REDIS_DB)
        r = r.pubsub()

        channel = 'radio.%s' % (radio_id)
        r.subscribe(channel)
        Logger().log.debug("subscribing to %s" % (channel))
        for m in r.listen():
            Logger().log.debug('emitting %s' % m)
            self.emit('radio_event', m)

def handle(environ, start_response):
    if environ['PATH_INFO'] == '/status/':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ["OK"]
    
    return socketio_manage(environ, {'/radio': RadioNamespace})

