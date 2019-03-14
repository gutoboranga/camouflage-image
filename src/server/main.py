import tornado.ioloop
import tornado.web

from server import create_app

app = create_app()
app.listen(5000)

print('> Running on port 5000')

tornado.ioloop.IOLoop.current().start()
