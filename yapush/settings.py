from os.path import abspath, dirname
import os

APP_MODE = os.environ.get('DJANGO_MODE', False)
PRODUCTION_MODE = ( APP_MODE == 'production' )
DEVELOPMENT_MODE = ( APP_MODE == 'development' )
LOCAL_MODE = not ( PRODUCTION_MODE or DEVELOPMENT_MODE )

HOST = '0.0.0.0'
PORT = 9000
CERT_FILE = '/etc/nginx/ssl/server.crt'
KEY_FILE = '/etc/nginx/ssl/server.key'

REDIS_HOST = 'localhost'
REDIS_DB = 0

if PRODUCTION_MODE:
    REDIS_HOST = 'yas-sql-01'
    REDIS_DB = 2
    
PROJECT_ROOT = abspath(dirname(__file__))
LOG_DIRECTORY = os.path.join(PROJECT_ROOT, 'logs/')
LOG_FILENAME = os.path.join(LOG_DIRECTORY, 'yapush.log')


AUTH_SERVER_KEY = '0VortuhIf23U5ZtD2XLVVG1xbNLBO2HPuogUROFRMn99ZWhcieezPNxFgaCYnhzH'
if PRODUCTION_MODE:
    AUTH_SERVER = 'https://api.yasound.com/api/v1/user_authenticated/'
elif DEVELOPMENT_MODE:
    AUTH_SERVER = 'http://dev.yasound.com/api/v1/user_authenticated/'
else:
    AUTH_SERVER = 'http://localhost:8000/api/v1/user_authenticated/'
