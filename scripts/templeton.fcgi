#!python
import inspect
import os.path
import sys
import web

sys.path.append('.')

print 'import'
from server import app

web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
app.run()
