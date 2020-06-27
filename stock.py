import yfinance as yf
import requests
import threading

exitFlag = False


def exitInput():
    global exitFlag
    while not exitFlag:
        inputMessage = input("Enter exit to stop the program: ")
        if inputMessage == "exit":
            exitFlag = True


def process(stockList):
    global exitFlag
    stockClassList = []
    for tick in stockList:
        stockClassList.append(Stock(tick))
    while not exitFlag:
        for stockClass in stockClassList:
            stockClass.scanNextOpportunity()
    for stockClass in stockClassList:
        if stockClass.currentPosition == "sold":
            continue
        else:
            stockClass.sell()


def isHammer(firstBar, secondBar):
    if firstBar["Close"] > secondBar["Open"] and firstBar["Open"] <= secondBar["Close"]:
        return True
    else:
        return False


def isBelowSMA(movingAverage, currentPrice):
    if movingAverage < currentPrice:
        return False
    else:
        return True


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.currentPosition = "idle"
        self.stopLoss = 0
        self.target = 0
        self.history = {}
        self.twentySMA = False
        self.tenSMA = False

    def fetchCurrentPrice(self):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" \
              "&symbol=" + self.ticker + "&interval=1min&apikey=ZA0L5BE0MXAE37QV"
        resp = requests.get(url)
        data = resp.json()
        openPrice = data[0]['Meta Data']['Time Series (1min)'][0]['1. open']
        closePrice = data[0]['Meta Data']['Time Series (1min)'][0]['4. close']
        currentPrice = (openPrice+closePrice)/2
        return currentPrice

    def fetchHistoricData(self, period, interval):
        stockInfo = yf.Ticker(self.ticker)
        stockHistory = stockInfo.history(period=period, interval=interval)
        print(stockHistory.iloc[[-1]]["Open"])
        return stockHistory

    def buy(self):
        self.currentPosition = "bought"
        print("Bought at " + str(self.fetchCurrentPrice()))

    def sell(self):
        self.currentPosition = "sold"
        print("Sold at " + str(self.fetchCurrentPrice()))

    def calculateSMA(self, period, currentPrice):
        periodString = str(period) + "d"
        stockPrices = self.fetchHistoricData(periodString, "1d")
        runningSum = 0
        i = 1
        while i < period:
            runningSum += stockPrices.iloc[[i]]["Close"]
            i += 1
        runningSum += currentPrice
        movingAverage = runningSum / period
        print(movingAverage)
        return movingAverage

    def buySignal(self):
        currentPrice = self.fetchCurrentPrice()
        todayBar = self.fetchHistoricData("1d", "5m")
        hammerFlag = isHammer(todayBar.iloc[[-1]], todayBar.iloc[[-2]])
        if hammerFlag:
            twentySMA = self.calculateSMA(20, currentPrice)
            if isBelowSMA(twentySMA, currentPrice):
                tenSMA = self.calculateSMA(10, currentPrice)
                if isBelowSMA(tenSMA, currentPrice):
                    return True
        return False

    def sellSignal(self):
        currentPrice = self.fetchCurrentPrice()
        twentySMACalc = self.calculateSMA(20, currentPrice)
        tenSMACalc = self.calculateSMA(10, currentPrice)
        twentySMAStatus = isBelowSMA(twentySMACalc, currentPrice)
        if twentySMAStatus and self.twentySMA:
            self.twentySMA = False
            return True
        elif not twentySMAStatus:
            self.twentySMA = True
        tenSMAStatus = isBelowSMA(tenSMACalc, currentPrice)
        if tenSMAStatus and self.tenSMA:
            self.tenSMA = False
            return True
        elif not tenSMAStatus:
            self.tenSMA = True
        return False

    def scanNextOpportunity(self):
        if self.currentPosition == "bought":
            if self.sellSignal():
                self.sell()
        else:
            if self.buySignal():
                self.buy()


"""
def buyingSetup(ticker):
    while True:
        if buySignal(ticker):
            buy(ticker)
            break
        else:
            continue
def sellingSetup(ticker):
    while True:
        if sellSignal(ticker):
            sell(ticker)
            break
        else:
            continue
def sellSignalCrap(ticker):
    global sellingStatus
    currentPrice = fetchCurrentPrice(ticker)
    twentySMA = api.calculateSMA(20, ticker, currentPrice)
    tenSMA = api.calculateSMA(10, ticker, currentPrice)
    try:
        indexInfo = sellingStatus.index(ticker)
        movingAverageStatus = sellingStatus[indexInfo]
        twentySMAStatus = api.isBelowSMA(twentySMA, currentPrice)
        if twentySMAStatus and movingAverageStatus["twentySMA"]:
            sellingStatus[indexInfo]["twentySMA"] = False
            return True
        elif not twentySMAStatus:
            sellingStatus[indexInfo]["twentySMA"] = True
        tenSMAStatus = api.isBelowSMA(tenSMA, currentPrice)
        if tenSMAStatus and movingAverageStatus["tenSMA"]:
            sellingStatus[indexInfo]["tenSMA"] = False
            return True
        elif not tenSMAStatus:
            sellingStatus[indexInfo]["tenSMA"] = True
        return False
    except ValueError:
        movingAverageStatus = {"twentySMA": False, "tenSMA": False}
        sellingStatus.append(movingAverageStatus)
        return False
def agenda(ticker):
    buyingSetup(ticker)
    sellingSetup(ticker)
"""

if __name__ == '__main__':
    stockString = input("Enter the stocks to watch: ")
    stockListInput = stockString.split()
    t = threading.Thread(target=exitInput)
    process(stockListInput)
    t.start()


