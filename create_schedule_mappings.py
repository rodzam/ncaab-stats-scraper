#!/usr/bin/python
##############################################################
# Program name: NCAA Basketball Stats Scraper (Schedule Mapping Module)
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

# Import modules and libraries
import scraperfunctions
import scrapersettings
import csv
from bs4 import BeautifulSoup

if (scrapersettings.map_schedule == 1):
    print "Generating schedule mappings"
    # Create the file headings
    schedule_mappingfile_w = open(scrapersettings.schedule_mappingfile, "w")
    schedule_mappingfile_w.writelines("game_id\thome_team_id\taway_team_id\tdate\tneutral_site\tgame_link\n")

    # Grab data
    # Parse our mappings file to get our list of teams
    team_mapping = scraperfunctions.get_team_mappings()

    # Create the schedule
    schedule_list = [] # Create an empty list for storing all of our games
    for value, team in enumerate(team_mapping): # For each team in our dictionary
        if scrapersettings.debugmode == 1: print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
        try:
            team_mainpage_data = scraperfunctions.grabber(team_mapping[team][1], scrapersettings.params, scrapersettings.http_header) # Grab the main page for each team
        except:
            print "Error getting data. Moving on to next game."
            continue
        team_mainpage_data_soup = BeautifulSoup(team_mainpage_data) # Soupify that page
        gamelinks = [] # Create a blank list for each game
        for link in team_mainpage_data_soup.find_all('a'): # Locate all links in the document
            if "game/index/" in link.get('href'): # If they contain a URL segment suggesting it is a game...
                game_link = str(scrapersettings.domain_base + link.get('href')).split("?")[0] # Strip out any URL variables since we don't need them
                try:
                    opponent_id = link.find_previous("td").find_previous("td").find("a").get('href').split("?org_id=")[1]
                except:
                    opponent_id = 0
                opponent_text = link.find_previous("td").find_previous("td").get_text().encode('utf-8').strip()
                if "@" in opponent_text: # Checks if home or away; note: if it's in a neutral site, this distinction may not be accurate (but a neutral site is flagged). Assumes all games against non-D-I/III competition is at home.
                    home_team = opponent_id
                    away_team = team
                    if "<br/>" in str(link.find_previous("a").encode('utf-8').strip()):
                        neutral = "1"
                    else:
                        neutral = "0"
                else:
                    home_team = team
                    away_team = opponent_id
                    neutral = "0"
                date = link.find_previous("td").find_previous("td").find_previous("td").get_text() # Get the date for the game
                game_id = game_link.split("/")[-1] # Get the game ID from the URL (last set of digits)
                schedule_list.append([game_id, home_team, away_team, date, neutral, game_link]) # Append all of this information to our master schedule list

    schedule_dict = dict([(case[0], (case[1:])) for case in schedule_list]) # Create a dictionary from our list so we don't have any duplicate entries
    for item in schedule_dict: # For each item on that list
        schedule_mappingfile_w.writelines(item + "\t" + str(schedule_dict[item][0]) + "\t" + str(schedule_dict[item][1]) + "\t" + str(schedule_dict[item][2]) + "\t" + str(schedule_dict[item][3]) + "\t" + str(schedule_dict[item][4]) + "\n") # Write to our mapping file
    print "Successfully generated schedule mappings"