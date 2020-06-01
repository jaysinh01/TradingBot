import flask
import alpaca_trade_api as tradeapi
from flask import jsonify
import yfinance as yf
#import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def stocksToWatch():
    stockString = input("Enter the stocks to watch: ")
    stockList = stockString.split()
    fetchHistoricData(stockList[0], "10m", "5m")
    currentPrice = 400.00
    calculateSMA(20, stockList[0], currentPrice)


def isHammer(firstBar, secondBar):
    if firstBar.close > secondBar.open and firstBar.open <= secondBar.close:
        return True
    else:
        return False


def fetchCurrentPrice(ticker):
    return 400.00


def buy(ticker):
    print("Bought at " + str(fetchCurrentPrice(ticker)))


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


def sell(ticker):
    print("Sold at " + str(fetchCurrentPrice(ticker)))


def agenda(ticker):
    buyingSetup(ticker)
    sellingSetup(ticker)


def buySignal(ticker):
    currentPrice = fetchCurrentPrice(ticker)
    todayBar = fetchHistoricData(ticker, "1d", "5m")
    hammerFlag = isHammer(todayBar[:][-1], todayBar[:][-2])
    if hammerFlag:
        twentySMA = calculateSMA(20, ticker, currentPrice)
        if isBelowSMA(twentySMA, currentPrice):
            tenSMA = calculateSMA(10, ticker, currentPrice)
            if isBelowSMA(tenSMA, currentPrice):
                return True
    return False


def sellSignal(ticker):
    currentPrice = fetchCurrentPrice(ticker)
    twentySMA = calculateSMA(20, ticker, currentPrice)
    tenSMA = calculateSMA(10, ticker, currentPrice)


def isBelowSMA(movingAverage, currentPrice):
    if movingAverage < currentPrice:
        return False
    else:
        return True


def calculateSMA(period, stockTic, currentPrice):
    periodString = str(period) + "d"
    stockPrices = fetchHistoricData(stockTic, periodString, "1d")
    runningSum = 0
    i = 1
    while i < period:
        runningSum += stockPrices["Close"][i]
        i += 1
    runningSum += currentPrice
    movingAverage = runningSum/period
    print(movingAverage)
    return movingAverage


def fetchHistoricData(stockTic, period, interval):
    stock = yf.Ticker(stockTic)
    stockHistory = stock.history(period=period, interval=interval)
    print(stockHistory["Close"])
    return stockHistory

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

#app.run()


if __name__ == '__main__':
    stocksToWatch()
