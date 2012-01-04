# This Source Code is subject to the terms of the Mozilla Public License
# version 2.0 (the "License"). You can obtain a copy of the License at
# http://mozilla.org/MPL/2.0/.

import web.httpserver
import os
import posixpath
import urllib

# Path to REST APIs.
APP_PREFIX = '/api/'

# Path on localhost to static HTML files.
# These will be served at the root.
STATIC_PATH = '../html'

LIBS_URL_PREFIX = '/templeton'

class MozStaticApp(web.httpserver.StaticApp):
    
    def __init__(self, environ, start_response, static_path=STATIC_PATH,
                 strip_prefix=''):
        web.httpserver.StaticApp.__init__(self, environ, start_response)
        self.static_path = static_path
        self.strip_prefix = strip_prefix
        if not self.static_path:
            self.static_path = os.getcwd()
        elif self.static_path[0] != '/':
            self.static_path = os.path.join(os.getcwd(), self.static_path)
    
    def translate_path(self, path):
        """Rather than applying the path against the cwd, apply it to
           static_path."""
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        if self.strip_prefix and path.find(self.strip_prefix) == 0:
            path = path[len(self.strip_prefix):]
        words = path.split('/')
        words = filter(None, words)
        path = self.static_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        path = os.path.normpath(path)
        return path


class MozStaticMiddleware:

    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        path = self.normpath(path)

        if path.startswith(APP_PREFIX):
            return self.app(environ, start_response)
        elif path.startswith(LIBS_URL_PREFIX):
            return MozStaticApp(environ, start_response, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server'), LIBS_URL_PREFIX)
        else:
            return MozStaticApp(environ, start_response)

    def normpath(self, path):
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith("/"):
            path2 += "/"
        return path2


def patch_middleware():
    """Patch the original StaticMiddleware."""
    web.httpserver.StaticMiddleware = MozStaticMiddleware


# Older templeton apps expected the middleware to be patched when this module
# was imported.  I realized this is probably poor form, so the project server
# template now calls patch_middleware() directly, but leaving this in for
# backwards compatibility.  It doesn't hurt to call it twice, and the explicit
# call in server.py discourages people from deleting the middleware import line,
# thinking it isn't used.
patch_middleware()

