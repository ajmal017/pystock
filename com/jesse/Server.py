import json
import os
import sys

os.chdir(os.path.join(os.path.realpath(__file__), ".."))
from abc import ABC


import tornado.ioloop
import tornado.web
import importlib
# from Tornado_study.fetcher.Rent import Rent
# sys.path.append(os.path.join(os.path.realpath(__file__), "./stock/fetcher"))
# sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__), "../../..")))
# from com.jesse.stock.fetcher.fetchBasic import Fetcher
Fetcher = importlib.import_module("stock.fetcher.fetchBasic").Fetcher
StockAnalysis = importlib.import_module("stock.res.StockAnalysis").StockAnalysis
from tornado import gen
# sys.path.append(os.path.join(os.path.realpath(__file__), "./stock/res"))


fetcher = Fetcher()
stockAnalysis = StockAnalysis("default")

class FetchBasicStock(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        response = fetcher.fetchGoodStocks()
        if len(stockAnalysis.stocks) == 0:
            stockAnalysis.fetchLocalData()
        stockAnalysis.fetchBasicData()
        stockAnalysis.fetchWeekInfo()
        self.write(response)

class DayGood(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        response = []
        for stock in stockAnalysis.stocks:
            if stock.goodGrowth():
                response.append(stock)
        self.write(json.dump(response, ensure_ascii=False))




class MainHandler(tornado.web.RequestHandler, ABC):
    def get(self):
        self.render("home.html")


def make_app():
    static_path_dir = os.path.dirname(os.path.realpath(__file__))
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path_dir}),
        (r'/fetchBasicStock', FetchBasicStock),
        (r'/dayGood', DayGood)
    ], static_path=os.path.join(os.path.dirname(__file__), "static"))


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
