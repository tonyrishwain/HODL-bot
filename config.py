#       config.py
# --------------------------------------------------------------------------------
#   This file is the configuration file for the HODL-bot application. Edit the
#   contents of this file to user preferred settings before starting the bot.
# --------------------------------------------------------------------------------


# import component

import ccxt


# define exchange used

exchange_id = 'binance' # see ccxt wiki for full list of available exchanges
exchange_class = getattr(ccxt, exchange_id)


# define exchange api key

exchange = exchange_class({
    'apiKey': '<api key>',
    'secret': '<api key secret>',
    'timeout': 30000,
    'enableRateLimit': True
})


# define portfolio params

portfolio = {

    # add coins and holding percentage according to the format below
    
    'BTC': 0.5,
    # BTC must be present for bot to function
    
    'ETH': 0.3
    'XRP': 0.1,
    'TUSD': 0.1
    
    # total must be equal to 1

}


# define frequency for jobs

interval = 5 # in minutes