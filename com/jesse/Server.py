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

class FetchDayData(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        if len(stockAnalysis.stocks) == 0:
            stockAnalysis.fetchLocalData()
        stockAnalysis.fetchBasicData()
        self.write("processing")

class FetchWeekData(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        if len(stockAnalysis.stocks) == 0:
            stockAnalysis.fetchLocalData()
        stockAnalysis.fetchWeekInfo()
        self.write("processing")

class FetchBasicStock(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        response = fetcher.fetchGoodStocks()
        self.write("processing")

class DayGood(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        response = []
        for stock in stockAnalysis.stocks:
            if stock.goodGrowth():
                response.append(stock)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(response)
        self.finish()




class MainHandler(tornado.web.RequestHandler, ABC):
    def get(self):
        self.render("home.html")


def make_app():
    static_path_dir = os.path.dirname(os.path.realpath(__file__))
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path_dir}),
        (r'/fetchBasicStock', FetchBasicStock),
        (r'/FetchDayData', FetchDayData),
        (r'/FetchWeekData', FetchWeekData),
        (r'/dayGood', DayGood)
    ], static_path=os.path.join(os.path.dirname(__file__), "static"))


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
