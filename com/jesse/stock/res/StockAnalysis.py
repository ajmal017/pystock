from com.jesse.stock.res.Stock import Stock
from com.jesse.stock.res.CommonExecutor import CommonExecutor
import json
import datetime
import requests
import logging
import time
import re


class StockAnalysis:
    def __init__(self, executor: CommonExecutor):
        self.executor = executor
        self.GOOD_STOCKS = "./basicInfo/good_stocks.json"
        self.stocks = []

    def fetchLocalData(self):
        self.stocks = []
        with open(self.GOOD_STOCKS, "r") as goodStocks:
            try:
                stocks = json.load(goodStocks)
                for stock in stocks:
                    self.stocks.append(Stock(stock))
                    pass
            except:
                print("get data error")

    def fetchBasicData(self):
        # url =
        # response = requests.get(url).text
        # response = '181009 22.05 21.82 22.12 21.26 628633'
        # pattern = re.compile(r'[0-9]{0,6}\s\d{0,2}\.\d{0,2}\s\d{0,2}\.\d{0,2}\s\d{0,2}\.\d{0,2}\s\d{0,2}\.\d{0,2}\s\d*')
        # pattern.findall(response)
        pattern = re.compile(r'[0-9]{0,6}\s\d{0,2}\.\d{0,2}\s\d{0,2}\.\d{0,2}\s\d{0,2}\.\d{0,2}\s\d{0,2}\.\d{0,2}\s\d*')
        for index, stock in enumerate(self.stocks):
            if index % 20 == 0:
                time.sleep(5)
                print("processing---sleeping for 5 second")
            print("processing---" + str(round((index + 1) / len(self.stocks) * 100, 2)) + "%")
            try:
                url = 'http://data.gtimg.cn/flashdata/hushen/daily/18/' + stock.stock_name + '.js?visitDstTime=1'
                response = requests.get(url).text
                url2 = 'http://data.gtimg.cn/flashdata/hushen/daily/19/' + stock.stock_name + '.js?visitDstTime=1'
                response2 = requests.get(url2).text
                response = response + "    " + response2
                data = pattern.findall(response)
                stock.setData(data)
                stock.fibonacci()
            except Exception as err:
                print(err)
            # print(stock.data)
            # print(len(stock.data))
        # stamp = datetime.datetime.utcnow()
        # timestamp = (stamp - datetime.datetime(1970, 1, 1)).total_seconds()*1000
        # print(timestamp)
        # for stock in self.stocks:
        #     url = "https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json" \
        #           "&stock_code="+str(stock.stock_name)+"&step=3&start=&count=160&fq_type=front&timestamp="+str(round(timestamp))
        #     print(url)
        #     response = requests.get(url).text
        #     print(response)
        #     try:
        #         jsonData = json.loads(response)
        #         print([x["date"] for x in jsonData["mashData"]])
        #         print([x["date"] for x in sorted(jsonData["mashData"], key=lambda data: data["date"], reverse=True)])
        #         stock.setData(sorted(jsonData["mashData"], key=lambda data: data["date"], reverse=True))
        #         stock.fibonacci()
        #         print(stock.data[0]["price13"])
        #     except Exception as e:
        #         logging.exception(e)


def main():
    stockAnalysis = StockAnalysis(CommonExecutor())
    stockAnalysis.fetchLocalData()
    stockAnalysis.fetchBasicData()
    for stock in stockAnalysis.stocks:
        print("for stock=" + stock.stock_name)
        if stock.isThisStockGrowth():
            if stock.goodGrowth():
                print(stock.stock_name + "{增长中反弹确立*****}")
            if stock.power():
                print(stock.stock_name + "{增长中蓄势待发, 参考周线判定是否到位***}")
            if stock.distroy():
                print(stock.stock_name + "{增长中极限回调****}")
        else:
            if stock.goodGrowth():
                print(stock.stock_name + "{弱势中反弹确立，参考周线判定是否到位****}")


main()
