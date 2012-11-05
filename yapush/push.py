from gevent import Greenlet, monkey, pywsgi, queue
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
import datetime
import gevent
import json
import redis
import settings
import Cookie
import requests
from logger import Logger

monkey.patch_all()


class RadioNamespace(BaseNamespace):
    def recv_connect(self):
        Logger().log.debug('%s: RadioNamespace received connect' % (self.environ['REMOTE_ADDR']))

    def recv_disconnect(self):
        Logger().log.debug('%s: RadioNamespace received disconnect' % (self.environ['REMOTE_ADDR']))
        try:
            self.kill_local_jobs()
            self.disconnect(silent=True)
        except Exception, e:
            Logger().log.error(e)
        return True

    def recv_message(self, data):
        Logger().log.debug('%s: RadioNamespace received message: %s' % (self.environ['REMOTE_ADDR'], data))
            
    def on_subscribe(self, data):
        Logger().log.debug('%s: RadioNamespace received on_subscribe: %s' % (self.environ['REMOTE_ADDR'], data))
        
        radio_id = data['radio_id']
        self.spawn(self.listener, radio_id)
        
    def on_unsubscribe(self, data):
        Logger().log.debug('%s: RadioNamespace unsubscribe received: %s' % (self.environ['REMOTE_ADDR'], data))
        self.kill_local_jobs()
        
    def listener(self, radio_id):
        r = redis.StrictRedis(host=settings.REDIS_HOST, db=settings.REDIS_DB)
        r = r.pubsub()

        channel = 'radio.%s' % (radio_id)
        r.subscribe(channel)
        Logger().log.debug("%s: subscribing to %s" % (self.environ['REMOTE_ADDR'], channel))
        for m in r.listen():
            if m.get('type') == 'subscribe':
                continue
            self.emit('radio_event', m)

class UserNamespace(BaseNamespace):
    def recv_connect(self):
        Logger().log.debug('%s: UserNamespace received connect' % (self.environ['REMOTE_ADDR']))

    def recv_disconnect(self):
        Logger().log.debug('%s: UserNamespace received disconnect' % (self.environ['REMOTE_ADDR']))
        try:
            self.kill_local_jobs()
            self.disconnect(silent=True)
        except Exception, e:
            Logger().log.error(e)
        return True

    def recv_error(self, packet):
        Logger().log.debug('%s: UserNamespace received error' % (self.environ['REMOTE_ADDR']))
        try:
            self.disconnect(silent=True)
        except Exception, e:
            Logger().log.error(e)
        return True

    def recv_message(self, data):
        Logger().log.debug('%s: UserNamespace received message: %s' % (self.environ['REMOTE_ADDR'], data))
            
    def on_subscribe(self, data):
        Logger().log.debug('%s: UserNamespace - received on_subscribe: %s' % (self.environ['REMOTE_ADDR'], data))
        
        sessionid = data.get('sessionid')
        if not sessionid:
            Logger().log.debug('missing sessionid value')
            return
        
        payload = {
            'sessionid': sessionid,
            'key':settings.AUTH_SERVER_KEY
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(settings.AUTH_SERVER, data=json.dumps(payload), headers=headers, verify=False)
        if not r.status_code == 200:
            Logger().log.debug('user not authenticated: %d' % (r.status_code))
            return None
        result = r.text
        data = json.loads(result)
        user_id = data['user_id']
        self.spawn(self.listener, user_id)
        
    def on_unsubscribe(self, data):
        Logger().log.debug('%s: unsubscribe received: %s' % (self.environ['REMOTE_ADDR'], data))
        self.kill_local_jobs()
        
    def listener(self, user_id):
        r = redis.StrictRedis(host=settings.REDIS_HOST, db=settings.REDIS_DB)
        r = r.pubsub()

        channel = 'user.%s' % (user_id)
        r.subscribe(channel)
        Logger().log.debug("%s: subscribing to %s" % (self.environ['REMOTE_ADDR'], channel))
        for m in r.listen():
            if m.get('type') == 'subscribe':
                continue
            self.emit('user_event', m)

def handle(environ, start_response):
    path = environ['PATH_INFO'] 
    if path  == '/status/':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ["OK"]
    elif path.startswith('/socket.io'):
        return socketio_manage(environ, {'/radio': RadioNamespace, '/me': UserNamespace})

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ["OK"]

