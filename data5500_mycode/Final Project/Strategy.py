'''
The strategy class details how to run the evaluation
It contains the sma, mean, and rsi methods and the code how to evaluate the different methods
'''

import datetime

class Strategy:

    def __init__(self, sma_fast: int = 14, sma_slow: int = 30, mean_days: int = 20, mean_factor: float = 2.0, 
            rsi_days: int = 14, rsi_buy:float = 30.0, rsi_sell: float = 70.0, unit_size: int=1):
        self.__sma_fast = sma_fast
        self.__sma_slow = sma_slow
        self.__mean_days = mean_days
        self.__factor = mean_factor
        self.__rsi_days = rsi_days
        self.__rsi_buy = rsi_buy
        self.__rsi_sell = rsi_sell
        self.__unit_size = unit_size
        self.__dlist = []

#------------------ properties -----------------
    @property
    def dlist(self):
        return self.__dlist

    @dlist.setter
    def dlist(self, value):
        self.__dlist = value

#-------------------funcion-------------------

# Function:     mean
# Parameters:   values
# Purpose:      get the mean from a list of values

    def mean(self, values: list):
        if len(values) > 0:
            return sum(values)/len(values) 
        return 0.0

# Function:     stdev
# Parameters:   values
# Purpose:      get the standard deviation from a list of values

    def stdev(self, values: list):
        m = self.mean(values)
        total = 0.0
        for x in values:
            total += (x-m) ** 2
        return (total/len(values)) ** 0.5

# Function:     data_list
# Parameters:   data = a dictionary of values. The key is the date and the value is the stock price
#               start_date = the date when we should start evaluating the data. By default this is the entire set of data
# Purpose:      turn a dictionary into a list, sorted by stock price date 
# 
    def data_list(self, data: dict, start_date: datetime.date):

        lst = []    # this is where the new data will live

        # loop through the sorted keys and append data
        for k in sorted(data.keys()):
            if start_date is None or datetime.date.fromisoformat(k) > start_date:
                lst.append(data[k])
        self.__dlist = lst
        return lst

# Function:     sma_crossover
# Parameters:   arr = a list of values
# Purpose:      calculate whether to buy or sell based on an array of values using SMA crossover
#               SMA crossover indcates a change in stock direction 
# 
    def sma_crossover(self, arr: list):
        # Eensure we have enough data for both SMAs
        # Need at least: (window size) + 1 extra to compute "previous" SMA
        if len(arr) < self.__sma_fast+1 or len(arr) < self.__sma_slow+1:
            return None

        sma_fast = self.mean(arr[-self.__sma_fast:])    
        sma_slow = self.mean(arr[-self.__sma_slow:])    
        sma_fast_previous = self.mean(arr[-1 - self.__sma_fast:-1])
        sma_slow_previous = self.mean(arr[-1 - self.__sma_slow:-1])

        # bullish cross-over
        # Fast SMA is rising faster than long-term prices
        if (sma_fast_previous <= sma_slow_previous) and (sma_fast > sma_slow):
            return "BUY"
        
        # bearish crossover
        # prices are falling faster than long-term prices
        elif (sma_fast_previous >= sma_slow_previous) and (sma_fast < sma_slow):   
            return "SELL"
        
        # Hold the stock
        else:
            return None

# Function:     mean_reversion
# Parameters:   arr = a list of values
# Purpose:      calculate whether to buy or sell based on a mean reversion strategy
#               Mean Reversion says prices tend to return to their average  

    def mean_reversion(self, arr: list):
        # ensure there is enough data to perform the analysis
        n = len(arr)
        if n < self.__mean_days+1:
            return None

        # select the past window excluding "yesterday"
        window = arr[-self.__mean_days-1:-1]

        # get the center and standard deviation for the window
        mean_window = self.mean(window)
        stdev_window = self.stdev(window)

        # define the threshold 
        low = mean_window - self.__factor * stdev_window
        high = mean_window + self.__factor * stdev_window

        # get yesterday's value and compare it to the thresholds
        yesterday = arr[-1]

        if yesterday < low:
            return "BUY"
        if yesterday > high:
            return "SELL"
        return None

# Function:     rsi
# Parameters:   arr = a list of values
# Purpose:      calculate whether to buy or sell based on a rsi strategy
                # RSI tells you if the market is overbought or oversold
                # It tells you whether buyers or sellers have controlled the market 

    def rsi(self, arr: list):

        # need enough data to calcluate rsi
        n = len(arr)
        if n < self.__rsi_days+1:
            return None

        start = n - self.__rsi_days
        gains = 0.0     # upwards movement
        losses = 0.0    # downward movement

        # check gains and losses over window
        for i in range(start, n):
            diff = arr[i] - arr[i - 1]
            if diff > 0:
                gains += diff
            else:
                losses -= diff 

        # covert totals to averages
        avg_gain = gains / self.__rsi_days
        avg_loss = losses / self.__rsi_days

        # compute the gain/loss ratio and rsi value
        if avg_loss == 0:
            rsi_val = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi_val = 100.0 - (100.0 / (1.0 + rs))

        if rsi_val < self.__rsi_buy:
            return "BUY"
        if rsi_val > self.__rsi_sell:
            return "SELL"
        return None

# Function:     action
# Parameters:   signal = results of each strategy on whether to buy, sell, or hold
#               price = yesterday's stock price
#               status = the current portfolio of the stock (number of units, cash, etc)
# Purpose:      action tracks (historically) the shares you would buy or sell based on the strategy

    def action(self, signal: str, price: float, status:dict):
        # no signal so hold stock
        if signal is None:
            return status

        # buy stock based on strategy
        elif signal == "BUY":
            status['units'] += self.__unit_size
            status['cash'] -= price*self.__unit_size

        # sell stock based on strategy
        elif signal == "SELL":
            status['units'] -= self.__unit_size
            status['cash'] += price*self.__unit_size
        return status

# Function:     evaluate_strategies
# Parameters:   None
# Purpose:      this function tests all three strategies, looping over the data set and calculating the signals
#               each strategy is evaluated 1 day at a time
#               stock is bought and sold using the action function (called from this function)

    def evaluate_strategies(self):
        #  Initialize the info 
        sorted_list = self.__dlist
        n = len(sorted_list)
        status = {
            'sma': {'units': 0, 'cash': 0.0, 'unrealized': 0.0},
            'mean': {'units': 0, 'cash': 0.0, 'unrealized': 0.0},
            'rsi': {'units': 0, 'cash': 0.0, 'unrealized': 0.0}
        }

        # not enough data so exit
        if n < 2:
            return status

        # make sure our sma parameters are correctly defined
        if self.__sma_fast > self.__sma_slow:
            temp = self.__sma_fast
            self.__sma_fast = self.__sma_slow
            self.__sma_slow = temp
        
        # loop over all available data
        for i in range(1, n):

            # grab the price information of the last day in the window
            price = sorted_list[i]

            # if there's enough data, evaluate sma and buy or sell based on the window's results
            # need +2 because of the window plus yesterday's value
            if i >= self.__sma_slow+2:
                past_data = sorted_list[i-self.__sma_slow-1:i]
                signal = self.sma_crossover(past_data)
                status["sma"] = self.action(signal, price, status["sma"])

            # if there's enough data, evaluate mean and buy or sell based on the window's results
            if i >= self.__mean_days+1:
                past_data = sorted_list[i-self.__mean_days-1:i]
                signal = self.mean_reversion(past_data)
                status["mean"] = self.action(signal, price, status["mean"])

            # if there's enough data, evaluate rsi
            if i >= self.__rsi_days+1:
                past_data = sorted_list[i-self.__rsi_days-1:i]
                status["rsi"] = self.action(self.rsi(past_data), price, status["rsi"])

        # get yesterday's price
        last_price = sorted_list[-1]

        best_method = None
        best_value = None

        # figure out which strategy is ahead as of yesterday. 
        # Use yesterday's price to calculate what gains/losses we haven't account for in currently held stock
        for s in status:
            # compute unrealized using final price
            status[s]["unrealized"] = status[s]["units"] * last_price
            status[s]["total"] = status[s]["cash"] + status[s]["unrealized"] 

            # best stock is the one with the highest cash + unrealized gains   
            if best_method is None or status[s]['total'] > best_value:
                best_method = s
                best_value = status[s]['total']
        status['best'] = best_method
        return status

# Function:     recommendation
# Parameters:   None
# Purpose:      this function provides a recommendation on whether to buy, sell, or hold stock for each of the three strategies
# 
    def recommendation(self):

        sorted_list = self.__dlist
        n = len(sorted_list)

        status = {
            'sma': None,
            'mean': None,
            'rsi': None
        }

        # not enough data so exit
        if n < 2:
            return status

        if self.__sma_fast > self.__sma_slow:
            start = self.__sma_fast
        else:
            start = self.__sma_slow

        price = sorted_list[-1]                 # yesterday's price

        # sma recommendation
        past_data = sorted_list[-start-1:]      # the past data
        status["sma"] = self.sma_crossover(past_data)
        
        # mean reversion recommendation
        past_data = sorted_list[-self.__mean_days-1:]  #          
        status["mean"] = self.mean_reversion(past_data)

        # rsi recommendation 
        past_data = sorted_list[-self.__rsi_days-1:]            
        status["rsi"] = self.rsi(past_data)
        return status

