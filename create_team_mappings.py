#!/usr/bin/python
##############################################################
# Program name: NCAA Basketball Stats Scraper (Team Mappings Module)
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

# Import modules and libraries
import scraperfunctions
import scrapersettings
from bs4 import BeautifulSoup

if (scrapersettings.map_teams == 1):
    print "Generating team mappings"
    # Create the file headings
    team_mappingfile_w = open(scrapersettings.team_mappingfile, "w")
    team_mappingfile_w.writelines("team_id\tteam_name\tteam_url\n")

    # Grab data
    # Download the page with the list of teams
    teamlist_data = scraperfunctions.grabber(scrapersettings.start_url, scrapersettings.params, scrapersettings.http_header) # Get data from main page
    teamlist_data_soup = BeautifulSoup(teamlist_data) # Soupify that data

    # Create a mapping for teams
    for link in teamlist_data_soup.find_all('a'): # For each hyperlink on the page
        if "team/index/" + str(scrapersettings.year_index) + "?org_id=" in link.get('href'): # If the hyperlink contains this string (limiting it only to team pages)
            team_id = str(link.get('href').split("team/index/" + str(scrapersettings.year_index) + "?org_id=")[1]) # Get the team ID from the URL
            team_name = str(link.get_text()) # Get the text associated with the hyperlink
            team_url = str(scrapersettings.domain_base + link.get('href')) # Get the URL and append the base domain
            team_mappingfile_w.writelines(str(team_id) + "\t" + str(team_name) + "\t" + str(team_url) + "\n") # Add lines to our TSV file for archival purposes
    print "Successfully generated team mappings"
