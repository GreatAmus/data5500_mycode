'''
Class object for COVID data
This class is used to store the data returned from the COVID API
Functions include saving data and analysing data
'''

import json
import cloudscraper # pip install cloudscraper

class CovidData:
    def __init__(self, state):
        self.__state = state
        self.__base_api = "https://api.covidtracking.com"
        self.__month_data = {}
        self.__data = []
        self.__nodata = False

    # Each state is a separate instance of the class
    @property
    def state(self):
        return self.__state

    # Error handling for states where there is no data
    @property
    def nodata(self):
        return self.__nodata

    @nodata.setter
    def nodata(self, val):
        self.__nodata = val

    # I probably didn't need to make this accessible but just in case we wanted to expand it to the newer data sets
    @property
    def base_api(self):
        return self.__base_api
    
    # Data returned from the API
    @property
    def data(self):
        return self.__data

    # Parse the data into a sublist based on months/years
    # Required for analysis where we want to examine groups of data instead of daily rates
    def create_sublist(self):
        key = ""
        sub_list = {}
        for day in self.data:
            key = str(day['date'])[0:6] # Get month and year
            sub_list[key] = sub_list.get(key,0)+day['positiveIncrease']          
        return sub_list

    # Retreive data from the API and parse it into month/year data
    def retrieve_data(self):
        self.dict = {}
        scraper = cloudscraper.create_scraper()
        url = f"https://api.covidtracking.com/v1/states/{self.state}/daily.json"
        response = scraper.get(url)
        self.__data = response.json()

        self.__month_data = self.create_sublist()
        self.nodata = not self.data_exists()

    # Check to see if the state actually has covid data. Some do not
    def data_exists(self):
        return self.daily_average() > 0

    # Save the raw JSON data to a file
    def save_data(self, file_path):
        with open(f"{file_path}/{self.state}.json", "w") as file:
            json.dump(self.data, file, indent = 3)

    # Save the analytic information to a file
    def save_analysis(self, file_path, data):
        with open(f"{file_path}/{self.state}_analysis.json", "w") as file:
            json.dump(data, file, indent = 3)

    # Get the daily average of covid rates
    def daily_average(self):
        if self.nodata:
            return 0
        positive_cases = [d['positiveIncrease'] for d in self.data]
        return sum(positive_cases)/len(positive_cases) if len(positive_cases) > 0 else 0

    # Get the day with the highest number of covid cases
    def highest_day(self):
        if self.nodata: # Chat suggested adding a handler (in the class file) where the data is empty
            return None

        high = ''
        count = 0
        for day in self.data:
            if day['positiveIncrease'] > count:
                high = day['date']
                count = day['positiveIncrease']
        return high

    # Get the day with the highest number of covid cases
    def no_covid(self):
        if self.nodata: # Chat suggested adding a handler where the data is empty
            return None
        zero_days = [d['date'] for d in self.data if d['positiveIncrease']== 0]
        return max(zero_days) if zero_days else None
    
    # Highest month-year of cases
    def month_highest_increase(self):
        if self.nodata: # Chat suggested adding a handler where the data is empty
            return None

        highest = max(self.__month_data, key=self.__month_data.get)      
        return(highest)

    # Lowest month-year of cases
    def month_lowest_increase(self):
        if self.nodata:   # Chat suggested adding a handler where the data is empty
            return None
            
        lowest = min(self.__month_data, key=self.__month_data.get)       
        return(lowest)


