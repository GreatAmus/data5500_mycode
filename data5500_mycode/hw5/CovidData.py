'''
Class object for COVID data
This class is used to store the data returned from the COVID API
Functions include saving data and analysing data
'''

import json
import requests

class CovidData:
    def __init__(self, state):
        self.__state = state
        self.__base_api = "https://api.covidtracking.com"
        self.__month_data = {}
        self.__data = []

    # Each state is a separate instance of the class
    @property
    def state(self):
        return self.__state

    # I probably didn't need to make this accessible but just in case we wanted to expand it to the newer data sets
    @property
    def base_api(self):
        return self.__base_api
    
    # Data returned from the API
    @property
    def data(self):
        return self.__data

    # Parse teh data into a sublist based on months/years
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
        self.__data = requests.get(f"{self.base_api}/v1/states/{self.state}/daily.json").json()
        self.__month_data = self.create_sublist()

    # Check to see if the state actually has covid data. Some do not
    def data_exists(self):
        return self.daily_average() > 0

    # Save teh raw jason data to a file
    def save_data(self, file_path):
        with open(f"{file_path}/{self.state}.json", "w") as file:
            json.dump(self.data, file, indent = 3)

    # Save the analytic information to a file
    def save_analysis(self, file_path, data):
        with open(f"{file_path}/{self.state}_analysis.json", "w") as file:
            json.dump(data, file, indent = 3)

    # Get the daily average of covid rates
    def daily_average(self):
        positive_cases = []
        for day in self.data:
            positive_cases.append(day['positiveIncrease'])
        return sum(positive_cases)/len(positive_cases)

    # Get the day with the highest number of covid cases
    def highest_day(self):
        high = ''
        count = 0
        for day in self.data:
            if day['positiveIncrease'] > count:
                high = day['date']
                count = day['positiveIncrease']
        return high

    # Get the day with the highest number of covid cases
    def no_covid(self):
        for day in self.data:
            if day['positiveIncrease'] == 0:
                return day['date']
        return 'None'
    
    # Highest month-year of cases
    def month_highest_increase(self):
        highest = max(self.__month_data, key=self.__month_data.get)      
        return(highest)

    # Lowest month-year of cases
    def month_lowest_increase(self):
        lowest = min(self.__month_data, key=self.__month_data.get)       
        return(lowest)


