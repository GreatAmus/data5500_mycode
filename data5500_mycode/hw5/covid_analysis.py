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

Chatgpt link:
https://chatgpt.com/share/68b7ad55-ef54-8010-be66-4f7bff88b3f9
Checking to see if chat thinks I met the requirements:
https://chatgpt.com/share/68b7ae6c-868c-8010-9b7f-8c7ed35a4274

'''

from pathlib import Path
from CovidData import *

# Constants - Colors for formating text and months for dates
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
COLORS = {'bold':'\033[1m', 'end': '\033[0m'}

# I stored all of the state values in a separate file to make it easy to use. This funciton reads the state information into a list
# file-path is where the directory of the state file
def get_states(file_path):
    with Path(f"{file_path}/states_territories.txt").open() as file:
        states = [state.rstrip() for state in file]
    return states

# The API stores dates as YYYYMMDD
# The format_date helper function takes a date from the API and converts it to Month DD, YYYY
def format_date(d : str):
    d = str(d)          # The API returns a number so this needs to be converted
    year = d[0:4]       # Strip the date into its 3 components
    month = int(d[4:6])
    day = int(d[6:])
    return(f"{MONTHS[month-1]} {day}, {year}")  # Format the date and return it

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
#               format_method: how to format the printed stat 
def print_stat(intro_string, stat, format_method): 
    if stat is None:     # The data anlaysis result matches the expected error message
        print(intro_string, 'No data found for this statistic.')
    elif format_method == 'date': # Format the data as Mon DD, YYYY
        print(intro_string, format_date(stat))
    elif format_method == 'month': # Format the data as Mo YYYY
        print(intro_string, format_month_year(stat))
    else:
        print(intro_string, stat)
    return

# Gather stat information and print the stat information per state
def gather_stats(data, file_path):
    # These are the data anlaytics requested by the problem along with the specified header
    print(f"{COLORS['bold']}State name: {data.state.upper()}{COLORS['end']}")
    question1 = "Average number of new daily confirmed cases for the entire state dataset:"
    question2 = "Date with the highest new number of covid cases:"
    question3 = "Most recent date with no new covid cases:"
    question4 = "Month and Year, with the highest new number of covid cases:"
    question5 = "Month and Year, with the lowest new number of covid cases:"

    # If there is data, print the answer to the requested stat and answer to the requested stat

    data_analysis = {
            'State': data.state,
            'Average': data.daily_average(),
            'Highest': data.highest_day(),
            'No covid': data.no_covid(),
            'Increase': data.month_highest_increase(),
            'Lowest': data.month_lowest_increase()
        }
    print(question1 , data_analysis['Average'])
    print_stat(question2, data_analysis['Highest'], 'date')
    print_stat(question3, data_analysis['No covid'], 'date')
    print_stat(question4, data_analysis['Increase'], 'month')
    print_stat(question5, data_analysis['Lowest'], 'month')

    data.save_analysis(file_path, data_analysis)   # Save the analysis to a file
    
    print()
    return

# Get the covid informaiton for a specific state, analyze the data, save the data
def print_covid_info(state, file_path):
    data = CovidData(state)     # create an object for the state       
    data.retrieve_data()        # Use the API to get the data
    gather_stats(data, file_path)  # Gather the stats and print them
    data.save_data(file_path)   # Save the data to a file
    return

# get the code's relative path for saving json files and loading state info
file_path = Path(__file__).parent

# load all state info from file
states = get_states(file_path)

# print required header
print("Covid confirmed cases statistics")

# loop over each state, loading the info and printin the stats
for s in states:
    print_covid_info(s, file_path)
