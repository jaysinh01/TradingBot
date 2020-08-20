import alpaca_trade_api as tradeapi
from api_key_config import *

api = tradeapi.REST(API_KEY_ID, API_SECRET_KEY, base_url='https://paper-api.alpaca.markets')

def getLastQuote(symbol):
    return api.get_last_quote(symbol)

print((getLastQuote("AAPL").askprice + getLastQuote("AAPL").bidprice) )
