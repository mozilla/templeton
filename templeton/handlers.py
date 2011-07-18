try:
    import json
except:
    import simplejson as json
import posixpath
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


def get_json(func):
    """ Translates results of 'func' into a JSON request. """
    def wrap(*a, **kw):
        if web.ctx.path[-1] != '/':
            # redirect all api calls to slash-terminated pages, for
            # consistency
            raise web.seeother(posixpath.join(web.ctx.env['SCRIPT_NAME'],
                                              web.ctx.path) + '/' +
                               web.ctx.query)
        try:
            results = json.dumps(func(*a, **kw))
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        web.header('Content-Length', len(results))
        web.header('Content-Type', 'application/json; charset=utf-8')
        return results
    return wrap


class JsonHandler(object):
    """
    Deprecated; use decorators instead, allowing for mixed response types.
    """

    @get_json
    def GET(self):
        args, body = get_request_parms()
        return self._GET(args, body)

    def _GET(self, params, body):
        raise NotImplementedError
