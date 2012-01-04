#!python

# This Source Code is subject to the terms of the Mozilla Public License
# version 2.0 (the "License"). You can obtain a copy of the License at
# http://mozilla.org/MPL/2.0/.

import inspect
import os.path
import sys
import web

sys.path.append('.')

print 'import'
from server import app

web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
app.run()
