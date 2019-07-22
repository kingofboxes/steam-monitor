# Script to monitor player status on Steam.
# Used for avoiding certain players / stacks.

# Set URL of Steam user (must be public profile):
url = "https://steamcommunity.com/profiles/76561198042309013/"
dotabuff_url = "https://www.dotabuff.com/players/82043285"

##### PACKAGES ##### 
import requests                                 # package for downloading page
from bs4 import BeautifulSoup                   # import BeautifulSoup (parse downloaded page)
import time                                     # import delay function
from datetime import datetime, timedelta        # for timestamping

##### FUNCTIONS #####
# Scrapes the name using title tag.
def name_scrape():
    name = []
    url_title = str(soup.find(lambda tag:tag.name=="title" and "Steam Community" in tag.text))
    for c in url_title:
        if c is ':':
            curr = url_title.index(c)+2
            while url_title[curr] != '<':
                if url_title[curr] is '.' or url_title[curr] is '_' or url_title[curr].isalpha() is True:
                    name.append(url_title[curr])
                curr += 1
            break
        else:
            continue
    return "".join(name)

# Scrapes a div using a specific class name.
def div_scrape(custom_class):
    game = []
    results = str(soup.find_all('div', attrs={"class":custom_class}))
    for c in results:
        if c is ">":
            curr = results.index(c) + 1
            while results[curr] != "<":
                game.append(results[curr])
                curr += 1
            break
        else:
            continue
    return "".join(game)

# Scrapes the most recent game on Dotabuff page.
def dotabuff_scrape(dotabuff_url, headers):

    # Set up requirements for scraping.
    dotabuff_response = requests.get(dotabuff_url, headers=headers)
    dotabuff_soup = BeautifulSoup(dotabuff_response.text, "lxml")
    string_soup = str(dotabuff_soup)
    index = string_soup.find("datetime")
    datetime_str = string_soup[index:index+50]

    # Gets the date and time for the last match.
    last_match = []
    for c in datetime_str:
        if c is "\"":
            curr = datetime_str.index("\"") + 1
            while datetime_str[curr] != "\"":
                last_match.append(datetime_str[curr])
                curr += 1
            break
        else:
            continue
    last_match = "".join(last_match)

    # Reformats the date and time by removing + signs and adding spaces.
    formatted_str = []
    for c in last_match:
        if c is '-' or c is ':' or c.isdigit() is True:
            formatted_str.append(c)
        elif c is '+':
            break
        else:
            formatted_str.append(' ')
    formatted_str = "".join(formatted_str)

    # Turns the formatted time into a datetime object, and finds the current difference in time (after converting from GMT 00:00).
    time_diff = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S") - (datetime.strptime(formatted_str, "%Y-%m-%d %H:%M:%S") + timedelta(hours=10))

    # Returns a timedelta object.
    return time_diff
    

##### SCRIPT #####
# Sets the first run variable.
fr = 1

# Check status indefinitely.
while True:

    # Set the headers of a browser.
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # Download the page.
    response = requests.get(url, headers=headers)

    # Parse the downloaded page into BeautifulSoup and grab all the text.
    soup = BeautifulSoup(response.text, "lxml")

    # Give output a timestamp.
    timestamp = "\n[" + datetime.now().strftime('%H:%M:%S') + "]"
    
    # Print out monitoring message (if it's the first run).
    if fr is 1:
        print(timestamp)
        print("Currently Monitoring: " + name_scrape() + " (" + url + ")")

    # Checks if Steam page says the user is in-game.
    # If not, print a message and sleep for 5 minutes.
    print(timestamp)
    if str(soup).find("Currently In-Game") == -1:
        print("Player is currently not in-game!")

    # Otherwise, scrape the game that they're in.
    else:
        game = div_scrape("profile_in_game_name")
        print("Player is currently in-game!")
        print("Game: " + game)
        
        # If the scraped game is specified...
        if game == "Dota 2":
            print("Scraping latest Dotabuff details...")
            
            time_ago = dotabuff_scrape(dotabuff_url, headers)
            print("Last match was " + str(time_ago.seconds//3600) + " hours " + str(((time_ago.seconds//60)%60)) + " minutes" + " ago.")

    # Change first run to 0.
    fr = 0

    # Sleep for 5 minutes.
    time.sleep(300)
    continue