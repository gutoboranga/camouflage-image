import tornado.ioloop
import tornado.web

from handlers import CreateHandler, WakeUpHandler, ResultHandler

class Server(tornado.web.Application):

    def __init__(self):
        super(Server, self).__init__(self.get_handlers())

    def get_handlers(self):
        handlers = [
            (r"/", WakeUpHandler),
            (r"/create", CreateHandler),
            (r"/result/(.*)", tornado.web.StaticFileHandler, { "path": "./results"}),
        ]
        return handlers


def create_app():
    return Server()
    