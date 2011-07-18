import templeton.handlers
import templeton.middleware
import handlers
import web

urls = templeton.handlers.load_urls(handlers.urls)

app = web.application(urls, handlers.__dict__)


if __name__ == '__main__':
    app.run()
