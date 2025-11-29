'''
The results class is a helper class used to print information related to the evaluation and trades
'''

import os
import json

class Results:

    def __init__(self, path: str):
        self.__path = os.path.join(path, "results", "results.json") # path where the results will be saved
        self.__result_data = {} # the data from the evaluation
        self.strat_name = {'sma': 'Simple Moving Average Crossover', 'mean': 'Mean Reversion', 'rsi': 'Relative Strength Index'} # converts the acronyms to real words

# Function:     load_results
# Parameters:   None
# Purpose:      this loads all of the results data
#               I never use this function but left it in in case I needed it for something

    def load_results(self):        
        with open(self.__path, "r") as f:
            data = json.load(f)
        self.__result_data = data
        return data

# Function:     print_results
# Parameters:   stock = the stock ticker we are printing
#               result = the result of an evaluation
# Purpose:      Prints the results of an evaluation of the three different strategies
# 
    def print_results(self, stock: str, result: dict):
        print()
        print(f"--- {stock} ---")

        # save the results into this class
        self.__result_data[stock] = result

        for r in result:                

            # r might be one of the three strategies or the best stock/strategy
            if r in ('sma', 'mean', 'rsi'):
                print(
                    f"\tEvaluation of {self.strat_name[r]}"
                    f"\n\t\t{'Cash':<10} : ${result[r]['cash']:>12,.2f}"
                    f"\n\t\t{'Unrealized':<10} : ${result[r]['unrealized']:>12,.2f}" 
                    f"\n\t\t{'Total':<10} : ${result[r]['total']:>12,.2f}"
                    )
        print(f"\tBest strategy for {stock}: {self.strat_name[result['best']]}")
        return

# Function:     overall_results
# Parameters:   None
# Purpose:      Review all the results to determine which strategy results in the best results
#               Also look at the stock and see which stock performed the best using the preferred strategy
# 
    def overall_results(self):

        # Track per-strategy totals across ALL stocks
        strat_total = {'sma': 0.0, 'mean': 0.0, 'rsi': 0.0}

        for stock, res in self.__result_data.items():
            for strat in ('sma', 'mean', 'rsi'):
                if strat in res and 'total' in res[strat]:
                    strat_total[strat] += res[strat]['total']

        # Find best overall strategy
        best_strategy = None
        best_strategy_total = None

        for strat, total in strat_total.items():
            if best_strategy is None or total > best_strategy_total:
                best_strategy = strat
                best_strategy_total = total

        # Find best stock for that best strategy
        best_stock = None
        best_stock_total = None

        if best_strategy is not None:
            for stock, res in self.__result_data.items():   # loop through stocks and results
                strat_res = res.get(best_strategy)
                if strat_res and 'total' in strat_res:
                    total = strat_res['total']
                    if best_stock is None or total > best_stock_total:
                        best_stock = stock
                        best_stock_total = total

        # print the results of the evaluation
        print()
        print(f"Total for sma:\t${strat_total['sma']:>10,.2f}")
        print(f"Total for mean:\t${strat_total['mean']:>10.2f}")
        print(f"Total for rsi:\t${strat_total['rsi']:>10,.2f}")
        print()
        self.__result_data['best strategy'] = best_strategy
        self.__result_data['best stock'] = best_stock
        return best_strategy, best_stock

# Function:     save_results
# Parameters:   None
# Purpose:      The assignment requires saving all results of the evaluation to results.json
# 

    def save_results(self):

        with open(self.__path, "w") as f:
            json.dump(self.__result_data, f, indent=3)

        print("\nSaved:", self.__path)

# Function:     print_recommendations
# Parameters:   signal = a dictionary telling you wehether to buy or sell per strategy Dictionary is stoc: {dictionary of strategies and signal}
#               best_strategy = an indication of what we should do based on the best performing strategy
# Purpose:      The assignment requires saving all results of the evaluation to results.json
#               Note that this is the best overall strategy and not the best for this particular stock - I wasn't sure which was the better approach
#   
    def print_recommendations(self, signal: dict, best_strategy: str):
        print('---RECOMMENDATIONS---')

        # loop through the different stocks stored in signal
        for stock in signal:
            print(f'\n=={stock}==')

            # look at each strategy and print its recommendation
            for strat in signal[stock]:
                recommend = signal[stock][strat] or "HOLD"
                print(f'\t{self.strat_name[strat]:<32} : {recommend}')

            # give the user the best recommendation based on the best strategy
            final = signal[stock][best_strategy] or 'HOLD'
            print(f"\t{'Recommendation':<32} : {final}")
