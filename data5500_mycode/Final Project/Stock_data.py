'''
The stock_data class holds all of the data related to stock.
Functions include retrieving the information from a CSV and saving the information 
'''
import os
from datetime import datetime, date

class Stock_data:
    def __init__(self, stock: str, path: str):
        self.__stock = stock                                        # specify which stock info we are storing in this instance
        self.__path = os.path.join(path, "data", f"{stock}.csv")   # path of where the old data can be found
        self.__data = {}                                            # the stock data as a dictionary where keys are the date and value is the item
        self.__last_update = None                                   # when was the data last updated (cuts down on the json file returned through the API)

# ------------ properties -----------------------
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value: dict):
        self.__data = value or {}

    # property for accessing the stock ticker related to the data
    @property
    def stock(self):
        return self.__stock

    @property
    def path(self):
        return self.__path

    # property to get when the data was last updated
    @property
    def last_update(self):
        return self.__last_update

    @last_update.setter
    def last_update(self, value):
        self.__last_update = value


#---------------- functions ----------------------------

# Function:     load_data
# Parameters:   None
# Purpose:      Open a CSV file of previously stored information and read the information
#               The CSV has one date and the corresponding price per line
#   
    def load_data(self):
        # If the data file doesn't exist, exit this function - all data will be retrieved from Alpaca
        if not os.path.exists(self.path):
            self.data = {}
            return

        # open the CSV and import the data
        data = {}
        with open(self.path) as file:
            for line in file:
                read_data = line.split(',')                 # data is in rows with a "date, value" format
                data[read_data[0]] = float(read_data[1])    # store the data with the date as the key and value as the item
        self.data = data                                    
        self.last_update = self.get_last_date()

        return 

# Function:     save_data
# Parameters:   None
# Purpose:      Open a CSV file to save retrieved data. If the path does not exist, all data will be saved
#               If the file exists, only new data is appended to the file
#    
    def save_data(self):
        
        # If the file does not exist, write all of the data to the file
        if not os.path.exists(self.path) or self.last_update is None:
            with open(self.path, "w") as f:
                for dt in self.data:
                    f.write(f"{dt},{self.data[date]}\n")
        else:
            # if the file exists, just append the new info based on the self.last_update information
            with open(self.path, "a") as f:
                for dt in self.data:
                    if self.last_update is None or date.fromisoformat(dt) > self.last_update:
                        f.write(f"{dt},{self.data[date]}\n")

        self.last_update = self.get_last_date()
        return

# Function:     get_last_date
# Parameters:   None
# Purpose:      Return the date of the newest entry in the data
#    
    def get_last_date(self):
        if self.__data:
            return date.fromisoformat(max(self.data.keys()))

# Function:     add_data
# Parameters:   new_data = the data returned from Alpaca
# Purpose:      Add new data to the data set, combining Alpaca data with CSV data
#    
    def add_data(self, new_data: dict):
        if new_data is None: 
            return

        for k in new_data:
            self.data[k] = new_data[k]

        return

