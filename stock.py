import yfinance as yf
import requests
import threading
from alpacaAPI import *

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
        if stockClass.currentPosition == "bought":
            stockClass.sell()
        else:
            print(stockClass.ticker + " was already sold or never purchased")


def isHammer(firstBar, secondBar):
    #firstbar bullish and secondbar bearish
    if firstBar["Close"][0] > secondBar["Open"][0] > secondBar["Close"][0] >= firstBar["Open"][0]:
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
        #consists of order classes
        self.order = []
        self.twentySMA = False
        self.tenSMA = False

    def fetchCurrentPrice(self):
        """url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" \
              "&symbol=" + self.ticker + "&interval=1min&apikey=ZA0L5BE0MXAE37QV"
        resp = requests.get(url)
        data = resp.json()
        openPrice, closePrice = 0, 0
        print(data)
        for dummy, candle in data["Time Series (1min)"].items():
            openPrice = float(candle['1. open'])
            closePrice = float(candle["4. close"])
            print(openPrice)
            print(closePrice)
            break"""
        """minutesCandles = self.fetchHistoricData("1d", "1m")
        openPrice = minutesCandles.iloc[[-1]]["Open"][0]
        closePrice = minutesCandles.iloc[[-1]]["Close"][0]
        currentPrice = (openPrice+closePrice)/2"""
        previousQuote = getLastQuote(self.ticker)
        currentPrice = (previousQuote.askprice + previousQuote.bidprice)/2
        return currentPrice

    def fetchHistoricData(self, period, interval):
        stockInfo = yf.Ticker(self.ticker)
        stockHistory = stockInfo.history(period=period, interval=interval)
        #print(stockHistory.iloc[[-1]]["Open"])
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
            runningSum += stockPrices.iloc[[i]]["Close"][0]
            i += 1
        runningSum += currentPrice
        movingAverage = runningSum / period
        #print(movingAverage)
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
        # Before: only one buy opportunity
        # Now: Scans for buy in opportunity every scan
        if self.buySignal():
            self.buy()
        elif self.currentPosition == "bought":
            if self.sellSignal():
                self.sell()
        else:
            self.isStockBought()
            self.scanNextOpportunity()

    def isStockBought(self):



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
    t.start()
    process(stockListInput)
"""
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" \
          "&symbol=AAPL&interval=1min&apikey=ZA0L5BE0MXAE37QV"
    resp = requests.get(url)
    data = resp.json()
    openPrice, closePrice = 0, 0
    for dummy, candle in data["Time Series (1min)"].items():
        openPrice = float(candle['1. open'])
        closePrice = float(candle["4. close"])
        print(openPrice)
        print(closePrice)
        break
    currentPrice = (openPrice + closePrice) / 2
    print(currentPrice)
    print(data["Time Series (1min)"])
    """


