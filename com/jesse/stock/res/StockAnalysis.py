from com.jesse.stock.res.Stock import Stock
from com.jesse.stock.res.CommonExecutor import CommonExecutor
import json
import datetime
import requests
import logging

class StockAnalysis:
    def __init__(self, executor: CommonExecutor):
        self.executor = executor
        self.GOOD_STOCKS = "./basicInfo/good_stocks.json"
        self.stocks = [Stock("sz300272")]

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
        stamp = datetime.datetime.utcnow()
        timestamp = (stamp - datetime.datetime(1970, 1, 1)).total_seconds()*1000
        print(timestamp)
        for stock in self.stocks:
            url = "https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json" \
                  "&stock_code="+str(stock.stock_name)+"&step=3&start=&count=160&fq_type=front&timestamp="+str(round(timestamp))
            print(url)
            response = requests.get(url).text
            print(response)
            try:
                jsonData = json.loads(response)
                print([x["date"] for x in jsonData["mashData"]])
                print([x["date"] for x in sorted(jsonData["mashData"], key=lambda data: data["date"], reverse=True)])
                stock.setData(sorted(jsonData["mashData"], key=lambda data: data["date"], reverse=True))
                stock.fibonacci()
                print(stock.data[0]["price13"])
            except Exception as e:
                logging.exception(e)


def main():
    stockAnalysis = StockAnalysis(CommonExecutor())
    stockAnalysis.fetchBasicData()

main()
