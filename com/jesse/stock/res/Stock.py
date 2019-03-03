class Stock:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.data = []

    def setData(self, data):
        self.data = data

    def fibonacci(self):
        for index, value in enumerate(self.data):
            if index < (len(self.data) - 13):
                total13price = 0

                for i in self.data[index:index+13]:
                    if index == 0:
                        print(i["date"])
                        print(i["kline"]["close"])
                    total13price = total13price + float(i["kline"]["close"])
                total13price = total13price/13
                self.data[index]["price13"] = total13price
            if index < (len(self.data) - 34):
                total34price = 0
                for i in self.data[index:index + 34]:
                    total34price = total34price + float(i["kline"]["close"])
                total34price = total34price / 34
                self.data[index]["price34"] = total34price
            if index < (len(self.data) - 55):
                total55price = 0
                for i in self.data[index:index + 55]:
                    total55price = total55price + float(i["kline"]["close"])
                total55price = total55price / 55
                self.data[index]["price55"] = total55price
            if index < (len(self.data) - 144):
                total144price = 0
                for i in self.data[index:index + 144]:
                    total144price = total144price + float(i["kline"]["close"])
                total144price = total144price / 144
                self.data[index]["price144"] = total144price

