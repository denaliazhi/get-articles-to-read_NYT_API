# This script allows the user to retrieve X articles from within a given week using the NYT Article Search API. 

# Import libraries to be used
import requests
import json
import pandas as pd

url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# Process to get valid API key from user:

# Initialize indicator
valid = False

while valid == False:

    # Direct the user to input their API key. You can get your own, here: https://developer.nytimes.com/get-started
    apikey = input("Please enter your API key:")

    # Test parameters
    parameters = { 'begin_date' : 20210802, 'end_date' : 20210802, 'api-key' : apikey}
    
    r = requests.get(url, parameters)
    status = r.status_code

    if status == 200:
        print("Your API key is valid.")
        valid = True

    else:
        print("Error: {status}. Your API key '{key}' is not valid.".format(status=status, key=apikey))

# Direct the user to input their desired search term
start = input("Please enter the start date (yyyy/mm/dd) for the week that you want to get articles from:")

import datetime

# Calculate the end date from user's inputted start date
year = int(start.split("/")[0])
month = int(start.split("/")[1])
day = int(start.split("/")[2])

days = datetime.timedelta(7) # Timespan is one week
end = datetime.date(year, month, day) + days

# Reformat start and end dates to be passed as parameters
start = str(datetime.date(year, month, day)).replace('-','')
end = str(end).replace('-','')

# Direct the user to input their desired number of articles
n = int(input("How many articles would you like to see?"))

import math

# Calculate how many pages to retrieve based on user's input
pages_needed = int(math.ceil(n/10))

# Initialize pagination
page = 1

# Extract two pieces of information for each article
headings =  ['headline', 'abstract', 'web_url']
table = pd.DataFrame(columns = headings)

while page < pages_needed + 1: # Get X pages of results

    parameters = { 'begin_date' : start, 'end_date' : end, 'api-key' : apikey, 'page' : page }
    r = requests.get(url, parameters) # Send a request for the page specified

    data = json.loads( r.text )
    articles = data['response']['docs'] # Array of articles returned
        
    i = 0
    while i < len(articles): # Review each article on the page
        row = [0, 1, 2]
        for key in articles[i].keys():
            if key == "headline":
                row[0] = articles[i][key]['main']
            elif key == "abstract":
                row[1] = articles[i][key]
            elif key == "web_url":
                row[2] = articles[i][key]
        length = len(table)
        table.loc[length] = row # Update the table with this article's data in a new row
        i = i + 1

    page = page + 1 # Move on to the next page

    import time
    time.sleep(7)

# Output resulting list of articles with their information to user
print("%i articles retrieved." % (n))
while i < n :
    print("""[HEADLINE #{number}] '{headline}'
    [SUMMARY] '{summary}'
    [GO TO] {url}\n"""
    .format(number = i+1, headline = table['headline'][i], summary = table['abstract'][i], url = table['web_url'][i]))
