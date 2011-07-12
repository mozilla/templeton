import templeton
import handlers
import web

urls = templeton.load_urls(handlers.urls)

app = web.application(urls, handlers.__dict__)


if __name__ == '__main__':
    app.run()
