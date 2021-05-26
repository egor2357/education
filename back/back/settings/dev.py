from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.137.100']

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1', '192.168.137.3']