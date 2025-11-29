''' 
This is the bot that controls the whole program so that it can be cron-jobbed to run each day. 
Autotrader does the following: 
1) pulls the stock information, 
2) evaluates stock over a range of time to see the best method of guessing profit (default is 3 years) 
3) finds whether you should buy or sell stock based on the best method of evaluating profit
4) executes a trade

Autotrader prints all of the informaiton to the console for review. This is the brains of the operation

'''
from Alpaca_API import Alpaca_API
from Stock_data import Stock_data
from Results import Results
from Strategy import Strategy
from datetime import datetime, date, timedelta, timezone

class AutoTrader:

    def __init__(self, file_path: str, stocks: list, market_API: str, trade_API: str, key: str, secret: str, start_date: str | date | None = None, units: int = 1):
        # These variables are all used to call the Alpaca API for trading and market data
        # Most of them are enrivronmental variables and defaults that could be changed if the program was enhanced further with things like "Srong Buy" or "Strong Sell"
        # The instructions did not say how many shares to buy per trade so we default to 1
        self.__file_path = file_path
        self.__market_api = market_API
        self.__trade_api = trade_API
        self.__key = key
        self.__secret = secret
        self.__stocks = stocks
        self.__units = units
        self.__start_date = self.normalize_time(start_date)

        # These are all used to store data and result information later in the program
        self.__alpaca = None
        self.__strategy = {}
        self.__stock_info = {}
        self.__results = None

#---- Properties for variables I thought users might want to change ----- 
    @property 
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        self.__file_path = value 

    @property 
    def market_api(self):
        return self.__market_api

    @market_api.setter
    def market_api(self, value):
        self.__market_api = value 

    @property 
    def trade_api(self):
        return self.__trade_api

    @trade_api.setter
    def trade_api(self, value):
        self.__trade_api = value 

    @property 
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        self.__start_date = self.normalize_time(value) 

    @property 
    def stocks(self):
        return self.__stocks

    @stocks.setter
    def stocks(self, value):
        self.__stocks = value 

    @property 
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value 


#---- Functions with execute controlling the entire program flow ----- 

# Function:     execute
# Parameters:   None
# Purpose:      This runs the entire operation and is a bot simunlating a user selected user options:
#               1) grabs saved data, updating it with the newest info
#               2) evaluates trading strategis based on a specified timefram. Default is 3 years
#               3) print the results of the evaluation
#               4) check whether we should buy or sell stock (selling without owning is allowed)
#               5) execute a paper trade for the stock and prints account balances

    def execute(self):

        # Evaluation strategy names
        strat_name = {'sma': 'Simple Moving Average Crossover', 'mean': 'Mean Reversion', 'rsi': 'Relative Strength Index'}

        #properly format the start date for the evaluation range    
        if self.start_date is None:
            self.start_date = date.today() - timedelta(days=365 * 3)
        
        # Initiate instances of the class objects that are used to store stock info and evaluation info
        self.__alpaca = Alpaca_API(self.market_api, self.trade_api, self.__key, self.__secret, self.start_date)
        self.__results = Results(self.file_path)

        # loop through the stocks and evaluate how well the trading strategies are performing
        for stock in self.stocks:
            self.__stock_info[stock] = self.get_data(stock)     # get the data
            strat_results = self.evaluate(stock)                # evaluate the performance
            self.print_results(stock, strat_results)            # print the results

        # Grab the best strategy
        best_strategy, best_stock = self.__results.overall_results()
        print("Best strategy:", strat_name[best_strategy])
        print("Best stock using best strategy:", best_stock)

        # per the assignment, save the results in results.json
        self.__results.save_results()

        # Allow paper trading
        if best_strategy is not None:
            self.paper_trade(best_strategy)

        return

# Function:     normalize_time
# Parameters:   dt = a potential date that needs to be convered to datetime.date format
#               dt could be none, a date, a string, or a datetime with timezones
# Purpose:      change all the forms of dates to a standarized datetime.date format

    def normalize_time(self, dt):
        if dt is None:
            return None
        if isinstance(dt, date) and not isinstance(dt, datetime):
            return dt
        if isinstance(dt, datetime):
             return dt.date()
        if isinstance(dt, str):
            s = dt.strip()

            # If it's a full datetime string, cut at the 'T'
            if "T" in s:
                s = s.split("T")[0]   # keep only the YYYY-MM-DD part
            return date.fromisoformat(s)

# Function:     get_data
# Parameters:   stock = the stock ticker we want to grab
# Purpose:      Get the stock data associated with a ticker. 
#               Information is first obtained from a CSV and then the API
#               API information is appended to the CSV file

    def get_data(self, stock: str):
        # Create a new instance of the stock class to store the stock data
        info = Stock_data(stock, self.file_path)
        last_update = info.get_last_date()

        # Find out when the data was last updated
        start = self.start_date
        if last_update is not None:
            if start is None or last_update > start:
                start = last_update

        # Update the stock data using Alpaca calls
        if self.__alpaca is not None:
            self.__alpaca.start_date = start
            updated_data = self.__alpaca.get_data(stock)
            info.add_data(updated_data)

        # save the informaiton to a CSV and return the stock data object
        info.save_data()
        return info

# Function:     evaluate
# Parameters:   stock - the stock ticker being evaluated
# Purpose:      Evaluate sma, mean, and rsi for performance on each stock
#               returns the evaluatoin results

    def evaluate(self, stock: str):
        strat = Strategy(unit_size=self.units)      # create a strategy instance
        strat.data_list(self.__stock_info[stock].data, self.start_date) # turn the data dictionary into a list 
        self.__strategy[stock] = strat              # save the data so its accessible outside of this function  
        return strat.evaluate_strategies()

# Function:     print_results
# Parameters:   stock = stock ticker that we want to print
#               results = the results of an evaluation using the Strategy class
# Purpose:      All this does is call the printer function in the Results class

    def print_results(self, stock: str, results: dict):
        # results: dict with 'sma', 'mean', 'rsi', 'best' etc.
        if self.__results is None:
            return None

        # print the results 
        self.__results.print_results(stock, results)
        return

# Function:     paper_trade
# Parameters:   best_strategy = which of the three trading strategies performed the best overall
# Purpose:      make a recommendation whether to buy or sell. 
#               The strategy used is based on which strategy is performing best

    def paper_trade(self, best_strategy: str):
        # Exit if there are not results as we don't know whether to buy or sell
        if self.__results is None:
            return

        # Loop through each stock and buy or sell based on the signal provided by the strategy    
        signal = {}
        for stock in self.stocks:
            if stock in self.__strategy:
                signal[stock] = self.__strategy[stock].recommendation()

        self.__results.print_recommendations(signal, best_strategy)     # print the signals returned
        self.__alpaca.trade_stock(signal, best_strategy, self.units)    # make a trade based on the returned signals
        self.__alpaca.print_account_totals()                            # print the account information 

        return
