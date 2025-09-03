'''
HW5: Web JSON API - Covid Cases
This assignment will provide you experience with Web JSON APIs and performing analysis with the data.
On this assignment you will perform some analysis on the number of covid cases for 50 states and 5 US territories.  
List of state codes here: states_territories.txtDownload states_territories.txt
Your program will use the publicly available API found here: https://covidtracking.com/data/api Links to an external site.

Your python program must perform the following calculations, for each state, and output the results to the console.  
The output for each country should be:
    Covid confirmed cases statistics
    State name: 
    Average number of new daily confirmed cases for the entire state dataset: (create a list of the positive increase of covid cases for each day, then take the average of the list)
    Date with the highest new number of covid cases:
    Most recent date with no new covid cases: 
    Month and Year, with the highest new number of covid cases: (sum the new number of cases for each day in a month, example March 2021)
    Month and Year, with the lowest new number of covid cases (example March 2020): 

Programming Requirements
    -Your program must use the API listed above to get JSON data.
    -The JSON data must be converted to a Python dictionary, and then the dictionary elements will be used to aggregate the data and perform the calculations.
    -Save the json data in a json file for each state/terrotitory as <state>.json
    -The program should produce:  the output shown above, and the json files.
'''

from pathlib import Path
from CovidData import *
import os

# Constants - Colors for formating text and months for dates
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
COLORS = {'bold':'\033[1m', 'end': '\033[0m'}

# I stored all of the state values in a separate file to make it easy to use. This funciton reads the state information into a list
# file-path is where the directory of the state file
def get_states(file_path):
    with open(f"{file_path}/states.txt") as file:
        states = [state.rstrip() for state in file]
    return states

# The API stores dates as YYYYMMDD
# The format_date helper function takes a date from the API and converts it to Month DD, YYYY
def format_date(d : str):
    d = str(d)          # The API returns floats so this needs to be converted
    year = d[0:4]       # Strip the date into its coponents
    month = int(d[4:6])
    day = int(d[6:])
    return(f"{MONTHS[month-1]} {day}, {year}")  # Format the date nad return it

# The API stores dates as YYYYMMDD
# The format_month_year helper function takes a date from the API and converts it to Month YYYY
def format_month_year(d : str):
    d = str(d)
    year = d[0:4]
    month = int(d[4:6])
    return(f"{MONTHS[month-1]} {year}") 

# Print the state's statistics
# AS does not have any data so we need a message if the data analysis cannot be compeleted
# Parameters:   intro-string: The string that explains the stat gathered
#               stat: results of the data analysis
#               no_data: what msg the data anlysis returns if it did not find relevant data
#               no_data_msg: what to print if the data field is empty
#               format_index: how to format the printed stat 
def print_stat(intro_string, stat, no_data, no_data_msg, format_index): 
    if stat == no_data:     # The data anlaysis result matches the expected error message
        print(intro_string, no_data_msg)
    elif format_index == 0: # Format the data as Mon DD, YYYY
        print(intro_string, format_date(stat))
    else:                   # Format the data as Mon YYYY
        print(intro_string, format_month_year(stat))
    return

# Gather stat information and print the stat information per state
def gather_stats(data):
    # These are the data anlaytics requested by the problem along with the specified header
    print(f"{COLORS['bold']}State name: {data.state.upper()}{COLORS['end']}")
    question1 = "Average number of new daily confirmed cases for the entire state dataset:"
    question2 = "Date with the highest new number of covid cases:"
    question3 = "Most recent date with no new covid cases:"
    question4 = "Month and Year, with the highest new number of covid cases:"
    question5 = "Month and Year, with the lowest new number of covid cases:"

    # If there is data, print the answer to the requested stat and answer to the requested stat
    if data.data_exists():
        no_data = "This state did not report any covid cases"
        print(question1 ,data.daily_average())
        print_stat(question2, data.highest_day(), "", no_data, 0)
        print_stat(question3, data.no_covid(), "None", "All days had at least one 1 new COVID case.", 0)
        print_stat(question4, data.month_highest_increase(), "", no_data, 1)
        print_stat(question5, data.month_lowest_increase(), "", no_data, 1)

    # If the data was empty, return the appropriate message
    else:
        warning = "This state did not provide covid data."
        print(question1,warning)
        print(question2, warning)
        print(question3, warning)
        print(question4, warning)
        print(question5, warning)

    print()
    return

# Get the covid informaiton for a specific state, analyze the data, save the data
def print_covid_info(state, file_path):
    data = CovidData(state)     # create an object for the state       
    data.retrieve_data()        # Use the API to get teh data
    gather_stats(data)          # Gather the stats and print them
    data.save_data(file_path)   # Save teh data to a file
    return

# get the code's relative path for saving json files and loading state info
file_path = Path(__file__).parent

# load all state info from file
states = get_states(file_path)

# print required header
print("Covid confirmed statistics")

# loop over each state, loading the info and printin the stats
for s in states:
    print_covid_info(s, file_path)
