'''
The Alpaca API class access the Alpaca API for market info and to make traders
#
'''
import requests
from datetime import datetime, date, timedelta, timezone, time

class Alpaca_API:
    def __init__(
        self, 
        alpaca_market_api: str,     # API for accessing pricing info
        alpaca_trade_api: str,      # API for making paper trades
        alpaca_key: str,            # API key used for Alpaca
        alpaca_secret: str,         # secret key for access to Alpaca
        start_date: date | None     # earliest point in time where we want to grab data. Default is 3 years
    ):

        #API info
        self.__key = alpaca_key
        self.__secret = alpaca_secret
        self.__market_api = alpaca_market_api
        self.__trade_api = alpaca_trade_api
        self.__start_date = start_date

#--------- properties ----------

    @property
    def start_date(self):
        return self.__start_date
    
    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    # returns the headers needed to access the API
    @property
    def headers(self):
        return {
            "APCA-API-KEY-ID": self.__key,
            "APCA-API-SECRET-KEY": self.__secret,
        }

#--------- functions ----------

# Function:     get_date
# Parameters:   None 
# Purpose:      Returns a date in a date with timezone format.
#               all dates are stored as datetime.date but Alpaca needs the timezone

    def get_date(self):
        if self.__start_date is None:
            dt = datetime.now(timezone.utc) - timedelta(days=365 * 3)
        else:
            dt = datetime.combine(self.__start_date, time.min).replace(tzinfo=timezone.utc)
        return dt.isoformat()

# Function:     get_data
# Parameters:   stock = stock ticker that we will retrieve
# Purpose:      Access the Alpaca API and returns the data
#               the data is returned as 'bars'. These bars are broken into dates and values
#               data is returned as a dictionary with the date as a key and value as the item

    def get_data(self, stock: str):
        stock_api = f"{self.__market_api}/stocks/{stock}/bars"

        # Required parameters for Alpaca API
        params = {
            "timeframe": "1Day",        # pull in incremenets of 1 day
            "limit": 2000,              # max itmsm returned
            "feed": "iex",              # free plan data
            "start": self.get_date()    # time window for the evaluation 
        }

        # get the stock info from the Alpaca API and convert to json
        try:
            data = requests.get(stock_api, headers=self.headers, params=params, timeout=30)
            data.raise_for_status()
            data = data.json()
    
        except Exception as e:
            print (f"Could not return stock data due to {e}")
            return None

        # Alpaca uses bars for the stock info
        bars = data.get("bars")

        # Keep only the date and close information. All of our evaluations will be based on the value of the stock on close
        data = {}
        if bars is None:
            return {}

        # Loop through the stock information and split it into date information, dropping the time information  
        for b in bars:
            #full iso date returned, but I need to change it into our standard of datetime.date format
            dt_time = b.get("t", "")
            dt = dt_time.split("T")[0] if "T" in dt_time else dt_time

            # add the data to our dictionary where the date is the key and teh close value is the item
            data[dt] = float(b.get("c"))

        return data

# Function:     trade_stock
# Parameters:   signal = an indicator whether to buy or sell on a per strategy basis
#               best_strategy = which strategy performs the best overall (which will determine the signal we use to buy or sell)
#               units = number of units to buy
# Purpose:      Loop over each stock and execute a paper trade to sell or buy stock based on the signal
                
    def trade_stock(self, signal: dict, best_strategy: str, units: int):
        url = f"{self.__trade_api}/orders"
        print("\n--- EXECUTING PAPER TRADES ---")

        # Loop over each stock and execute a Buy/Sell depending on the signal provided
        for stock, strat_signals in signal.items():
            action = strat_signals.get(best_strategy)        # do  you buy or sell based on the best performing strategy? 

            # If there isn't a buy or sell signal then hold the stock for now
            if action is None:
                print(f"{stock:<5} : Best strategy is to HOLD - no trade made.")
                continue
            
            # buy or sell the stock
            try:
                parameters = {
                    "symbol": stock,            # stock ticker
                    "qty": units,               # number of units to trade
                    "side": action.lower(),     # 'buy' or 'sell' based on signal
                    "type": 'market',           # I just used market here since it seemed the most common
                    "time_in_force": 'day',     # I just used good for the day. This could be expanded for more sophisticated buys
                }

                # get the order ID so we know the trade completed
                order = requests.post(url, headers=self.headers, json=parameters, timeout = 30)
                order.raise_for_status()
                data = order.json()

            except Exception as e:
                print(f"{stock}: Failed to place order because {e}")

            # print the order ID so we know the order took place
            print(f"{stock:<5} : Placed {action.upper()} {units} share(s). Order id: {data.get('id')}")

        return

# Function:     get_account
# Parameters:   None
# Purpose:      Grabs the account information from the alpaca API

    def get_account(self):
        url = f"{self.__trade_api}/account"
        resp = requests.get(url, headers=self.headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

# Function:     print_account_totals
# Parameters:   None
# Purpose:      Print the paper account balance so you can see (over time) the effects of our trades

    def print_account_totals(self):
        # print the account's cash, equity value, and buying power
        acct = self.get_account()
        cash = float(acct.get("cash", 0.0))
        equity = float(acct.get("equity", 0.0))
        buying_power = float(acct.get("buying_power", 0.0))

        # formatting
        print("\n--- PAPER ACCOUNT TOTALS ---")
        print(f"Cash:         ${cash:>11,.2f}")
        print(f"Equity:       ${equity:>11,.2f}")
        print(f"Buying power: ${buying_power:>11,.2f}")