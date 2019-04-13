import os

import requests
import json
import time


class Fetcher:

    def __init__(self):
        self.BASIC_INFO_STOCKS_JSON = os.path.join(os.path.dirname(__file__), "../res/basicInfo/stocks.json")
        self.GOOD_STOCKS = os.path.join(os.path.dirname(__file__), "../res/basicInfo/good_stocks.json")

    def fetchGoodStocks(self):
        with open(self.BASIC_INFO_STOCKS_JSON, "r") as jsonFile:
            stocks = json.load(jsonFile)
            for index, stock in enumerate(stocks):
                print("processing---" + str(round((index + 1) / len(stocks) * 100, 2)) + "%")
                self.__fetch_good_stocks(stock)
        return "not blocking"

    def fetchStockName(self):
        numberOfStock = self.__getCurrentStockNumber()
        totalFetchNumber = numberOfStock % 80 + 1
        print(totalFetchNumber)
        stocks = []
        for i in range(totalFetchNumber):
            responstTest = self.__fetchStockNameWithOffset(i)
            for stocksInfo in responstTest:
                stocks.append(stocksInfo[0])
        with open(self.BASIC_INFO_STOCKS_JSON, "w") as jsonFile:
            json.dump(stocks, jsonFile, ensure_ascii=False)

    def __getCurrentStockNumber(self):
        url = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0,1," \
              "100]]&callback=analysisTitle "
        response = requests.get(url)
        responseStr = response.text.split("analysisTitle")[1]
        responseStr = responseStr[:-2]
        responseStr = responseStr[2:]
        responseJson = json.loads(responseStr)
        return responseJson[0]["count"]

    def __fetchStockNameWithOffset(self, offset):
        if offset < 0:
            return []

        url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,' + str(
            offset) + ',' + str(offset + 1) + ',80]]&callback=analysisEachPage '
        responstStr = requests.get(url).text.split("analysisEachPage")[1]
        responseStr = responstStr[:-2]
        responseStr = responseStr[2:]
        responseJson = json.loads(responseStr)
        time.sleep(3)
        return responseJson[0]["items"]

    def __fetch_good_stocks(self, stock):
        url = "http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?ctype=4&type=0&code=" + stock
        responseText = requests.get(url).text
        try:
            responseJson = json.loads(responseText)
        except:
            return
        if len(responseJson) <= 5:
            return
        if responseJson[0]['mgjyxjl'] != "--" and responseJson[4]['mgjyxjl'] != "--":
            latestCash = float(responseJson[0]['mgjyxjl'])
            secondCash = float(responseJson[4]['mgjyxjl'])
            latestLiabilities = float(responseJson[0]['zcfzl'])
            secondLiabilities = float(responseJson[1]['zcfzl'])
            beforeCache = float(responseJson[1]['mgjyxjl'])
            if latestCash > 0 and latestLiabilities < secondLiabilities and latestCash > secondCash and beforeCache < latestCash:
                cut = latestCash - secondCash
                if cut / abs(secondCash) > 0.6:
                    self.__store_good_stock(stock)

    def __store_good_stock(self, stock):
        with open(self.GOOD_STOCKS, "r") as goodStocks:
            try:
                jsonArray = json.load(goodStocks)
            except:
                jsonArray = json.loads("[]")
            jsonArray.append(stock)
            with open(self.GOOD_STOCKS, "w") as file:
                json.dump(jsonArray, file, ensure_ascii=False)
