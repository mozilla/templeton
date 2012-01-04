# This Source Code is subject to the terms of the Mozilla Public License
# version 2.0 (the "License"). You can obtain a copy of the License at
# http://mozilla.org/MPL/2.0/.

try:
    import json
except:
    import simplejson as json
import posixpath
import StringIO
import urlparse
import web

""" URL fragment with which all dynamic requests should begin. """
API_PATH = '/api'

def load_urls(u):
    """ Load a list of URLs, ensuring they all start with API_PATH. """
    urls = []
    count = 0
    for i in u:
        if count % 2 == 0:
            path = i
            if path.find(API_PATH) != 0:
                path = API_PATH + path
            urls.append(path)
        else:
            urls.append(i)
        count += 1
    return urls


def get_request_parms():
    """ Parses search string and body as JSON. """
    try:
        body = json.loads(web.data())
    except (TypeError, ValueError):
        body = None
    return (urlparse.parse_qs(web.ctx.query[1:], True), body)


def redirect_api_if_needed():
    """ Redirects all api calls to slash-terminated pages, for
        consistency"""
    if web.ctx.path[-1] != '/':
        raise web.seeother(web.ctx.env.get('SCRIPT_FILENAME', '') +
                           web.ctx.path + '/' + web.ctx.query)


def json_response(func):
    """ Translates results of 'func' into a JSON request. """
    def wrap(*a, **kw):
        redirect_api_if_needed()

        try:
            results = json.dumps(func(*a, **kw))
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        web.header('Content-Length', len(results))
        web.header('Content-Type', 'application/json; charset=utf-8')
        return results
    return wrap


def png_response(func):
    """ Translates a PIL image into a PNG response. """
    def wrap(*a, **kw):
        redirect_api_if_needed()

        output = StringIO.StringIO()
        try:
            im = func(*a, **kw)
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise

        im.save(output, format="PNG")
        data = output.getvalue()
        web.header('Content-Length', len(data))
        web.header('Content-Type', 'image/png')
        return data
    return wrap
