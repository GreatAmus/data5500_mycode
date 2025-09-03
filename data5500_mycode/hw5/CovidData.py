import json
import requests

class CovidData:
    def __init__(self, state):
        self.__state = state
        self.__base_api = "https://api.covidtracking.com"
        self.__month_data = {}
        self.__data = []

    @property
    def state(self):
        return self.__state

    @property
    def base_api(self):
        return self.__base_api
    
    @property
    def data(self):
        return self.__data

    def create_sublist(self):
        key = ""
        sub_list = {}
        for day in self.data:
            key = str(day['date'])[0:6]
            sub_list[key] = sub_list.get(key,0)+day['positiveIncrease']
           
        return sub_list

    def retrieve_data(self):
        self.dict = {}
        self.__data = requests.get(f"{self.base_api}/v1/states/{self.state}/daily.json").json()
        self.__month_data = self.create_sublist()

    def data_exists(self):
        return self.daily_average() > 0

    def save_data(self, file_path):
        with open(f"{file_path}/{self.state}.json", "w") as file:
            json.dump(self.data, file, indent = 3)

    def daily_average(self):
        positive_cases = []
        for day in self.data:
            positive_cases.append(day['positiveIncrease'])
        return sum(positive_cases)/len(positive_cases)

    def highest_day(self):
        high = ''
        count = 0
        for day in self.data:
            if day['positiveIncrease'] > count:
                high = day['date']
                count = day['positiveIncrease']
        return high

    def no_covid(self):
        for day in self.data:
            if day['positiveIncrease'] == 0:
                return day['date']
        return 'None'
    
    def create_list(self):
        print(self.__data)

        key = ""
        sub_list = {}
        for day in self.data:
            key = str(day['date'])[0:6]
            sub_list[key] = sub_list.get(key,0)+day['positiveIncrease']
           
        return sub_list

    def month_highest_increase(self):
        highest = max(self.__month_data, key=self.__month_data.get)      
        return(highest)

    def month_lowest_increase(self):
        lowest = min(self.__month_data, key=self.__month_data.get)       
        return(lowest)


