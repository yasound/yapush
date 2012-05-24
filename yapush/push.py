from gevent import Greenlet, monkey, pywsgi, queue
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
import datetime
import gevent
import json
import logging
from logging.handlers import RotatingFileHandler
import redis
import settings

monkey.patch_all()

FORMAT = '%(asctime)-15s %(message)s'
formatter = logging.Formatter(FORMAT)

log = logging.getLogger('MyLogger')
log.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

file_handler = RotatingFileHandler(settings.LOG_FILENAME, maxBytes=1024*10, backupCount=10)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)


class RadioNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_subscribe(self, data):
        log.debug('receveid on_subscribe: %s' % (data))
        
        radio_id = data['radio_id']
        self.spawn(self.listener, radio_id)
        
    def on_unsubscribe(self, data):
        self.kill_local_jobs()
        
    def listener(self, radio_id):
        r = redis.StrictRedis(host=settings.REDIS_HOST, db=settings.REDIS_DB)
        r = r.pubsub()

        channel = 'radio.%s' % (radio_id)
        r.subscribe(channel)
        log.debug("subscribing to %s" % (channel))
        for m in r.listen():
            log.debug('emitting %s' % m)
            self.emit('radio_event', m)

def handle(environ, start_response):
    if environ['PATH_INFO'] == '/status/':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ["OK"]
    
    return socketio_manage(environ, {'/radio': RadioNamespace})

