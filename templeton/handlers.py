try:
    import json
except:
    import simplejson as json
import posixpath
import urlparse
import web

class JsonHandler(object):

    def GET(self):
        if web.ctx.path[-1] != '/':
            # redirect all api calls to slash-terminated pages, for
            # consistency
            raise web.seeother(posixpath.join(web.ctx.env['SCRIPT_NAME'],
                                              web.ctx.path) + '/' +
                               web.ctx.query)
        try:
            body = json.loads(web.data())
        except (TypeError, ValueError):
            body = None
        results = json.dumps(self._GET(urlparse.parse_qs(web.ctx.query[1:],
                                                         True), body))
        web.header('Content-Length', len(results))
        web.header('Content-Type', 'application/json; charset=utf-8')
        return results

    def _GET(self, params, body):
        raise NotImplementedError
