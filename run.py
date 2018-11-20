#       run.py
# --------------------------------------------------------------------------------
#   This file is the main program in the HODL-bot application. Execute this script
#   to start the bot.
# --------------------------------------------------------------------------------


# import components

from apscheduler.schedulers.blocking import BlockingScheduler
import config
from os import system


# define function to execute trader script

def run_rebal():
    system('/<path to>/trader.py')

    
# define and start scheduler of job

scheduler = BlockingScheduler()
scheduler.add_job(run_rebal, 'interval', minutes=config.interval)
scheduler.start()