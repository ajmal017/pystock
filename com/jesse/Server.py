import json
import os
from abc import ABC


import tornado.ioloop
import tornado.web
# from Tornado_study.fetcher.Rent import Rent
from com.jesse.stock.fetcher.fetchBasic import Fetcher
from tornado import gen
from com.jesse.stock.res.StockAnalysis import StockAnalysis

fetcher = Fetcher()
stockAnalysis = StockAnalysis()

class FetchBasicStock(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self, *args, **kwargs):
        response = yield fetcher.fetchGoodStocks()
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
