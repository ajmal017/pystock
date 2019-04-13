import os
from abc import ABC


import tornado.ioloop
import tornado.web
# from Tornado_study.fetcher.Rent import Rent





class MainHandler(tornado.web.RequestHandler, ABC):
    def get(self):
        self.render("home.html")


def make_app():
    static_path_dir = os.path.dirname(os.path.realpath(__file__))
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path_dir})
    ], static_path=os.path.join(os.path.dirname(__file__), "static"))


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
