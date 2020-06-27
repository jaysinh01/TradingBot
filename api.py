import flask
import alpaca_trade_api as tradeapi
from flask import jsonify
import yfinance as yf
#import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

sellingStatus = []

#stop loss to be added


def stocksToWatch():
    stockString = input("Enter the stocks to watch: ")
    stockList = stockString.split()
    fetchHistoricData(stockList[0], "1mo", "1d")
    currentPrice = 400.00
    #calculateSMA(20, stockList[0], currentPrice)







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
