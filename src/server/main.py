import os
import tornado.ioloop
import tornado.web

from server import create_app

app = create_app()

port = int(os.environ.get('PORT', 4000))
app.listen(port)

print('> Running on port {}'.format(port))

tornado.ioloop.IOLoop.current().start()
