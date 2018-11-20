#       rebalance.py
# --------------------------------------------------------------------------------
#   This file runs in the background to write to logs and create a trading matrix.
# --------------------------------------------------------------------------------


# import required components

import config
from datetime import datetime
from pytz import timezone
import pytz
import csv
import os
import math


# set current datetime stamp for logs

date_format='%m/%d/%Y %H:%M:%S %Z'
date = datetime.now(tz=pytz.utc)
date = date.astimezone(timezone('US/Pacific'))


# initialize connection to exchange API from config

portfolio = config.portfolio

exchange = config.exchange
markets = exchange.load_markets()
mkt_list = list(markets.keys())


# create empty dicts and lists for holding data

sell_mkts = {}
buy_mkts = {}
track_dict = {}

log_list = [date.strftime(date_format)]


# define functions

def get_price(coin):
    a = coin + '/USDT'
    try: return exchange.fetch_ticker(a)['info']['weightedAvgPrice']
    except: return float(exchange.fetch_ticker(coin + '/BTC')['info']['weightedAvgPrice']) * \
    float(exchange.fetch_ticker('BTC/USDT')['info']['weightedAvgPrice'])

def usd_value(coin_data):
    usd_total = 0
    for i in list(coin_data.keys()):
        usd = float(coin_data[i]['price']) * float(coin_data[i]['balance'])
        usd_total += usd
    return usd_total

def round_figs(num, sig_figs):
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0

    
# create iterable list of coins and empty dict for storing data from exchange API

coinlist = list(portfolio.keys())
coin_data = {}


# define headers for log.csv

log_head = ['DATE_TIME','PORTFOLIO_USD_VAL','PORTFOLIO_BTC_VAL']
for coin in coinlist:
    log_head.append(coin+'_TARG%')
    log_head.append(coin+'_BAL')
    log_head.append(coin+'_USD_VAL')
    
    
# add headers to log.csv if its empty

if os.stat('log.csv').st_size == 0:
    with open('log.csv', 'a') as csvloghandle:
        csvwrite = csv.writer(csvloghandle)
        csvwrite.writerow(log_head)
if os.stat('data.csv').st_size == 0:
    with open('data.csv', 'a') as csvdatahandle:
        csvwrite = csv.writer(csvdatahandle)
        csvwrite.writerow(['USD_VALUE','BTC_VALUE'])
        
        
# add headers to trade_tracker.csv if its empty

if os.stat('trade_tracker.csv').st_size == 0:
    with open('trade_tracker.csv', 'a') as csvtradehandle:
        csvwrite = csv.writer(csvtradehandle)
        csvwrite.writerow(['DATE/TIME','MARKET','TRADE TYPE','PRICE','USD PRICE','AMOUNT','USD VALUE','USD FEE'])

        
# dictionary to contain coin trade requirements

trade_req = {}


# calculate necessary change in balance per coin based on current price and holdings

for coin in coinlist:
    coin_data[coin] = {'price': get_price(coin), 'balance': exchange.fetchBalance()[coin]['total']}

port_value = usd_value(coin_data)
log_list.append(port_value)
log_list.append(float(port_value) / float(exchange.fetch_ticker('BTC/USDT')['info']['weightedAvgPrice']))

with open('data.csv', 'a') as csvdatahandle:
    csvwrite = csv.writer(csvdatahandle)
    csvwrite.writerow(log_list[1:])
        
for coin in coinlist:
    log_list.append(portfolio[coin]*100)
    log_list.append(coin_data[coin]['balance'])
    log_list.append(float(coin_data[coin]['balance']) * float(coin_data[coin]['price']))

for coin in coinlist:
    x = (port_value * portfolio[coin]) / float(coin_data[coin]['price'])
    trade_req[coin] = x - float(coin_data[coin]['balance'])

base_cur = '/BTC'

for coin in coinlist:
    for key in mkt_list:
        if key == coin + base_cur:
            # trade will only be queued for execution if trade amount > min trade * 5
            
            incl_sell = (trade_req[coin] * float(exchange.fetch_ticker(key)['info']['weightedAvgPrice']) < 0 - \
                         float(markets[key]['info']['filters'][2]['minNotional']) * 1.1) and (trade_req[coin] < 0 - \
                         float(markets[key]['info']['filters'][1]['minQty']) * 1.1)
            
            incl_buy = (trade_req[coin] * float(exchange.fetch_ticker(key)['info']['weightedAvgPrice']) > \
                        float(markets[key]['info']['filters'][2]['minNotional']) * 1.1) and (trade_req[coin] > \
                        float(markets[key]['info']['filters'][1]['minQty']) * 1.1)
            
            if incl_sell: sell_mkts[key] = round_figs(float(0 - trade_req[coin]),4)
            elif incl_buy: buy_mkts[key] = round_figs(float(trade_req[coin]),4)

                
                
for coin in coinlist:
    for key in (list(sell_mkts.keys())+list(buy_mkts.keys())):
        if key == coin + base_cur:
            track_dict[coin] = [date.strftime(date_format)]

for i in range(len(list(sell_mkts.keys()))):
    for coin in list(track_dict.keys()):
        if list(sell_mkts.keys())[i] == coin+base_cur:
            track_dict[coin].append(list(sell_mkts.keys())[i])
            track_dict[coin].append('sell')
            basepricetemp = float(exchange.fetch_ticker(list(sell_mkts.keys())[i])['info']['weightedAvgPrice'])
            track_dict[coin].append(basepricetemp)
            usdpricetemp = float(exchange.fetch_ticker(list(sell_mkts.keys())[i])['info']['weightedAvgPrice']) * float(exchange.fetch_ticker('BTC/USDT')['info']['weightedAvgPrice'])
            track_dict[coin].append(usdpricetemp)
            track_dict[coin].append(str(sell_mkts[list(sell_mkts.keys())[i]])[:10])
            usdvaltemp = float(sell_mkts[list(sell_mkts.keys())[i]]) * float(exchange.fetch_ticker(list(sell_mkts.keys())[i])['info']['weightedAvgPrice']) * float(exchange.fetch_ticker('BTC/USDT')['info']['weightedAvgPrice'])
            track_dict[coin].append(usdvaltemp)
            track_dict[coin].append(0.00075*usdvaltemp)
        
for i in range(len(list(buy_mkts.keys()))):
    for coin in list(track_dict.keys()):
        if list(buy_mkts.keys())[i] == coin+base_cur:
            track_dict[coin].append(list(buy_mkts.keys())[i])
            track_dict[coin].append('buy')
            basepricetemp = float(exchange.fetch_ticker(list(buy_mkts.keys())[i])['info']['weightedAvgPrice'])
            track_dict[coin].append(basepricetemp)
            usdpricetemp = float(exchange.fetch_ticker(list(buy_mkts.keys())[i])['info']['weightedAvgPrice']) * float(exchange.fetch_ticker('BTC/USDT')['info']['weightedAvgPrice'])
            track_dict[coin].append(usdpricetemp)
            track_dict[coin].append(str(buy_mkts[list(buy_mkts.keys())[i]])[:10])
            usdvaltemp = float(buy_mkts[list(buy_mkts.keys())[i]]) * float(exchange.fetch_ticker(list(buy_mkts.keys())[i])['info']['weightedAvgPrice']) * float(exchange.fetch_ticker('BTC/USDT')['info']['weightedAvgPrice'])
            track_dict[coin].append(usdvaltemp)
            track_dict[coin].append(0.00075*usdvaltemp)

with open('log.csv', 'a') as csvloghandle:
    csvwrite = csv.writer(csvloghandle)
    csvwrite.writerow(log_list)

with open('trade_tracker.csv', 'a') as csvtradehandle:
    csvwrite = csv.writer(csvtradehandle)
    for item in track_dict:
        csvwrite.writerow(track_dict[item])