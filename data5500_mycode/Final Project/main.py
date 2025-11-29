'''
Stock Market Trading Assignment
You must choose at least 10 stocks
    stocks: ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","DAL","XOM","PEP"]
Your analysis must include 3 trading strategies.  Mean Reversion and Simple Moving Average Crossover strategy examples can be found in the github repo. - Done. I use
    3 strategies: SMA, Mean, and RSI
Your program should implement short selling.  Meaning you can sell before you buy.  To implement this, add a sell variable to your program and allow it to sell without buying first.  Add the logic to the buy if statement to add to profits when your buy also (profit += sell - buy).  This logic will now be in your buy and your sell if statements.
    Done - you are not required to own stock before selling
Your program should save the data in csv files (i’ll let you decide the format/columns of the file)
    Done - see data folder
Your program should be able to save new data into the files.  Meaning, when I go to run your program, it should go get the latest data, update the files, and run new analysis.
    Done - append function runs adding only data after the last update
If your program detects a buy signal or sell signal on the last day in the data, print a message like “You should <buy or sell> this stock today”.
    Done - buy or sell signal published
Store your results to your strategy in a results.json, and specifically identify which stock and strategy made the most profit.
    Done
Your program must submit paper orders (not real orders) to an alpaca paper trading account.  For details on setting up an account visit: Paper Trading Specification - Documentation | AlpacaLinks to an external site.
    Done
Your program must run every weekday at 9amET, using crontab on your Linux server.  https://askubuntu.com/questions/2368/how-do-i-set-up-a-cron-jobLinks to an external site.  
    Done

Chat gpt links:
https://chatgpt.com/share/692b72d9-4e90-8010-b925-c45414305ff6

Full disclosure - work switched to a chat gpt enterprise account, which doesn't allow me to share with unauthenticated users. 
I recreated my chatgpt questions on a free chat gpt account.
'''

import os
from AutoTrader import AutoTrader
from dotenv import load_dotenv

# I previously used relative environments but it was causing issues with the cron job. I switched to an excplicit path to make the cron job work
#PATH = "/home/ubuntu/data5500_mycode/Final Project"
PATH = os.path.dirname(os.path.abspath(__file__))

# Load environment variables that are static but important information 
load_dotenv()
ALPACA_MARKET_API = os.environ.get("ALPACA_MARKET_URL", "")
ALPACA_TRADE_URL = os.environ.get("ALPACA_TRADE_URL", "")
ALPACA_KEY = os.environ.get("ALPACA_KEY", "")
ALPACA_SECRET = os.environ.get("ALPACA_SECRET", "")

# Establish the stocks we will be trading
stocks = ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","DAL","XOM","PEP"]

# run the automated trader program
trader = AutoTrader(
    file_path=PATH, 
    stocks=stocks, 
    market_API=ALPACA_MARKET_API, 
    trade_API=ALPACA_TRADE_URL, 
    key=ALPACA_KEY, 
    secret=ALPACA_SECRET,
    units=1
    )

trader.execute()