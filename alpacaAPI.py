import alpaca_trade_api as tradeapi
from api_key_config import *

api = tradeapi.REST(API_KEY_ID, API_SECRET_KEY, base_url='https://paper-api.alpaca.markets')

def getLastQuote(symbol):
    return api.get_last_quote(symbol)

print((getLastQuote("AAPL").askprice + getLastQuote("AAPL").bidprice))

def placeOrder(symbol, qty, side, type, time_in_force, limit_price, client_order_id):
    api.submit_order(
        symbol=symbol,
        side=side,
        type=type,
        qty= qty,
        time_in_force=time_in_force,
        order_class='simple',
        limit_price=limit_price,
        client_order_id=client_order_id
    )

def cancelOrder(client_order_id):
    api.cancel_order(client_order_id)


def getUpdatedOrder(client_order_id):
    return api.get_order(client_order_id)