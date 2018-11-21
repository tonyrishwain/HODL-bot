# HODL-bot

### Python project using [CCXT] (https://github.com/ccxt/ccxt).

This bot will automatically balance your cryptocurrency portfolio according to defined parameters at a defined frequency. The application is lightweight and has CSV logging capabilities for analyzing data, recording trades, and tracking performance.

Dependencies:
- Python 3
- [CCXT] (https://github.com/ccxt/ccxt)
- [APScheduler] (https://github.com/agronholm/apscheduler)

Features:
- Configurable portfolio contents and holding percentages
- Configurable rebalance frequency
- CSV log files for each of the following:
  - Portfolio overall state
  - Portfolio value tracking
  - Trade tracking

Usage:
- Copy the files in this repo to a local directory
- Edit config.py to your desired settings
- Edit the hashbang (#!) first line in trader.py
- Edit run.py to correctly point to trader.py script
- Run run.py (ideally in the background using screen or another application)
- Refer to csv log files for performance tracking

Notes:
- For a full list of supported exchanges refer to ccxt wiki
- BTC must be included as an asset for this program to function
- This program was developed and tested using Binance. Troubleshooting may be required when connecting other exchanges