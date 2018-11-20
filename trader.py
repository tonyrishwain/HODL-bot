#!/<path to>/python

# --------------------------------------------------------------------------------
#   ****IMPORTANT!****
#   Before starting the bot, it is REQUIRED to change the first line of this
#   script (line starting with '#!') to point to the installation of python that
#   contains the required dependencies.
# --------------------------------------------------------------------------------

#       trader.py
# --------------------------------------------------------------------------------
#   This script is triggered by run.py to execute trades.
# --------------------------------------------------------------------------------


# run rebalance.py

import rebalance


# define values used to make trades

exchange = rebalance.exchange
sell_mkts = rebalance.sell_mkts
buy_mkts = rebalance.buy_mkts
    
    
# execute sell orders

for symbol in list(sell_mkts.keys()):
    orderbook = exchange.fetch_order_book(symbol)
    exchange.create_market_sell_order(symbol, sell_mkts[symbol])
    
    
# execute buy orders

for symbol in list(buy_mkts.keys()):
    orderbook = exchange.fetch_order_book(symbol)
    exchange.create_market_buy_order(symbol, buy_mkts[symbol])