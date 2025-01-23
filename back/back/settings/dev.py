from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.137.100', '82.146.55.188']

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1', '192.168.137.3', '192.168.137.4']

WS_IP = 'ws://192.168.137.100:8765'