import os
import tornado.ioloop
import tornado.web

from server import create_app

app = create_app()
port = int(os.environ.get("PORT", 5000))
app.listen(5000)

# print('> Running on port 5000')

tornado.ioloop.IOLoop.current().start()
