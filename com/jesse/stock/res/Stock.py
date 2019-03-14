class Stock:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.data = []
        self.weekData = []

    def setData(self, data):
        # 190307 9.09 9.00 9.10 8.86 135903
        # [0] date
        # [1] open price
        # [2] close price
        # [3] top price
        # [4] low price
        # [5] amount
        # [6] price 13
        # [7] price 34
        # [8] price 55
        # [9] price 144
        self.data = data

    def fibonacciWeekData(self):
        for index, value in enumerate(self.weekData):
            if index < len(self.weekData):
                if index > 13:
                    price13 = 0
                    for i in self.weekData[index - 12:index + 1]:
                        price13 = price13 + float(i[2])
                    price13 = price13 / 13
                    self.weekData[index].append(str(price13))
                if index > 34:
                    price34 = 0
                    for i in self.weekData[index - 33:index + 1]:
                        price34 = price34 + float(i[2])
                    price34 = price34 / 34
                    self.weekData[index].append(str(price34))
                if index > 55:
                    price55 = 0
                    for i in self.weekData[index - 54:index + 1]:
                        price55 = price55 + float(i[2])
                    price55 = price55 / 55
                    self.weekData[index].append(str(price55))
                if index > 144:
                    price144 = 0
                    for i in self.weekData[index - 143:index + 1]:
                        price144 = price144 + float(i[2])
                    price144 = price144 / 144
                    self.weekData[index].append(str(price144))

    def fibonacci(self):
        for index, value in enumerate(self.data):
            # print(str(index) + str(value))
            if index > 13:
                price13 = 0
                for i in self.data[index - 12:index + 1]:
                    price13 = price13 + float(i.split(" ")[2])
                price13 = price13 / 13
                self.data[index] = self.data[index] + " " + str(round(price13, 2))
            if index > 34:
                price34 = 0
                for i in self.data[index - 33:index + 1]:
                    price34 = price34 + float(i.split(" ")[2])
                price34 = price34 / 34
                self.data[index] = self.data[index] + " " + str(round(price34, 2))
            if index > 55:
                price55 = 0
                for i in self.data[index - 54:index + 1]:
                    price55 = price55 + float(i.split(" ")[2])
                price55 = price55 / 55
                self.data[index] = self.data[index] + " " + str(round(price55, 2))
            if index > 144:
                price144 = 0
                for i in self.data[index - 143:index + 1]:
                    price144 = price144 + float(i.split(" ")[2])
                price144 = price144 / 144
                self.data[index] = self.data[index] + " " + str(round(price144, 2))

    # 大趋势多头
    # 判断144线是否拐头向上
    def isThisStockGrowth(self):
        try:
            latest = float(self.data[len(self.data) - 1].split(" ")[9])
            secondLatest = float(self.data[len(self.data) - 2].split(" ")[9])
            if latest > secondLatest:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

    # 反弹确立
    # 13天线在34上方，在55下方
    # 13天线是向上的
    def goodGrowth(self):
        try:
            latest13 = float(self.data[len(self.data) - 1].split(" ")[6])
            second13 = float(self.data[len(self.data) - 2].split(" ")[6])
            if latest13 > second13:
                latest34 = float(self.data[len(self.data) - 1].split(" ")[7])
                latest55 = float(self.data[len(self.data) - 1].split(" ")[8])
                if latest34 < latest13 < latest55:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as err:
            print(err)
            return False

    # 13天线纠结态
    # 连续5天，在13天线附近盘整
    def power(self):
        try:
            for index, i in enumerate(self.data[-5:]):
                closePrice = float(i.split(" ")[2])
                price13 = float(i.split(" ")[6])
                j = abs(price13 - closePrice)
                j = j / closePrice
                if j > 0.01:
                    break
                else:
                    if index == 4:
                        if j < 0.01:
                            return True
            return False
        except Exception as err:
            print(err)
            return False

    #破势接入调整
    def distroy(self):
        try:
            price = float(self.data[len(self.data)-1].split(" ")[2])
            price34 = float(self.data[len(self.data) - 1].split(" ")[7])
            price55 = float(self.data[len(self.data) - 1].split(" ")[7])
            price144 = float(self.data[len(self.data) - 1].split(" ")[7])
            second34 = float(self.data[len(self.data) - 2].split(" ")[7])
            second55 = float(self.data[len(self.data) - 2].split(" ")[7])
            second144 = float(self.data[len(self.data) - 2].split(" ")[7])
            if price34 >= second34 and price55 >= second55 and price144 >= second144 and price < price55:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

        # price = float(self.data[len(self.data)-1]).split(" ")[2])
        # price34 = float(self.data[len(self.data)-1].split(" ")[7])