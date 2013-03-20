#!/usr/bin/python
##############################################################
# Program name: NCAA Basketball Stats Scraper (Player Mapping and Summary Stats Module)
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

# Import modules and libraries
import scraperfunctions
import scrapersettings
import csv
import re
from bs4 import BeautifulSoup

if (scrapersettings.map_players == 1):
    # Create the file headings
    player_mappingfile_w = open(scrapersettings.player_mappingfile, "w")
    player_mappingfile_w.writelines("player_id\tteam_id\tplayer_name\n")

if (scrapersettings.summary_players == 1):
    # Create the file headings
    summary_player_data_w = open(scrapersettings.summary_player_data, "w")
    summary_player_data_w.writelines("player_id\tplayer_name\tteam_id\tteam_name\tjersey\tyear\tpos\theight\tplayed\tstarted\tminutes\tfgm\tfga\tfgpct\tthree_fgm\tthree_fga\tthree_fgpct\tft\tfta\tftpct\tpts\tptsavg\toffreb\tdefreb\ttotreb\trebavg\tast\tto\tstl\tblk\tfouls\tdbldbl\ttrpdbl\n")

if (scrapersettings.summary_teams == 1):
    # Create the file headings
    summary_team_data_w = open(scrapersettings.summary_team_data, "w")
    summary_team_data_w.writelines("team_id\tteam_name\tteam_minutes\tteam_fgm\tteam_fga\tteam_fgpct\tteam_three_fgm\tteam_three_fga\tteam_three_fgpct\tteam_ft\tteam_fta\tteam_ftpct\tteam_pts\tteam_ptsavg\tteam_offreb\tteam_defreb\tteam_totreb\tteam_rebavg\tteam_ast\tteam_to\tteam_stl\tteam_blk\tteam_fouls\tteam_dbldbl\tteam_trpdbl\topp_team_minutes\topp_team_fgm\topp_team_fga\topp_team_fgpct\topp_team_three_fgm\topp_team_three_fga\topp_team_three_fgpct\topp_team_ft\topp_team_fta\topp_team_ftpct\topp_team_pts\topp_team_ptsavg\topp_team_offreb\topp_team_defreb\topp_team_totreb\topp_team_rebavg\topp_team_ast\topp_team_to\topp_team_stl\topp_team_blk\topp_team_fouls\topp_team_dbldbl\topp_team_trpdbl\n")


if (scrapersettings.map_players == 1) or (scrapersettings.summary_players == 1) or (scrapersettings.summary_teams == 1):
    print "Generating player mappings and/or summary data for players and/or summary data for teams"
    # Grab data
    # Parse our mappings file to get our list of teams
    team_mapping = scraperfunctions.get_team_mappings()

    # Parse the stats table
    player_list = [] # Create an empty list for storing all of our players
    team_stats_total = []
    for value, team in enumerate(team_mapping): # For each team in our dictionary
        if scrapersettings.debugmode == 1: print "Processing team " + str(team) + " (" + str(value+1) + " of " + str(len(team_mapping)) + ")"
        roster_url = str(scrapersettings.domain_base) + "/team/stats?org_id=" + team + "&sport_year_ctl_id=" + str(scrapersettings.year_index)
        team_name = team_mapping[team][0]
        roster_page_data = scraperfunctions.grabber(roster_url, scrapersettings.params, scrapersettings.http_header) # Grab the main page for each team
        roster_page_data_soup = BeautifulSoup(roster_page_data)
        stat_grid = roster_page_data_soup.select('#stat_grid')

        # Get Player Data
        for rowno, row in enumerate(stat_grid[0].find('tbody').findAll('tr')):
            tds = row.findAll('td')
            player_id = tds[1].find('a').get('href').split('=')[-1]
            jersey = str(tds[0].get_text().encode('utf-8').strip())
            name = str(tds[1].find('a').get_text().encode('utf-8').strip())
            year = str(tds[2].get_text().encode('utf-8').strip())
            pos = str(tds[3].get_text().encode('utf-8').strip())
            height = str(tds[4].get_text().encode('utf-8').strip())
            played = str(tds[5].get_text().encode('utf-8').strip())
            started = str(tds[6].get_text().encode('utf-8').strip())
            minutes = str(tds[7].get_text().encode('utf-8').strip())
            fgm = str(tds[8].get_text().encode('utf-8').strip())
            fga = str(tds[9].get_text().encode('utf-8').strip())
            fgpct = str(tds[10].get_text().encode('utf-8').strip())
            three_fgm = str(tds[11].get_text().encode('utf-8').strip())
            three_fga = str(tds[12].get_text().encode('utf-8').strip())
            three_fgpct = str(tds[13].get_text().encode('utf-8').strip())
            ft = str(tds[14].get_text().encode('utf-8').strip())
            fta = str(tds[15].get_text().encode('utf-8').strip())
            ftpct = str(tds[16].get_text().encode('utf-8').strip())
            pts = str(tds[17].get_text().encode('utf-8').strip())
            ptsavg = str(tds[18].get_text().encode('utf-8').strip())
            offreb = str(tds[19].get_text().encode('utf-8').strip())
            defreb = str(tds[20].get_text().encode('utf-8').strip())
            totreb = str(tds[21].get_text().encode('utf-8').strip())
            rebavg = str(tds[22].get_text().encode('utf-8').strip())
            ast = str(tds[23].get_text().encode('utf-8').strip())
            to = str(tds[24].get_text().encode('utf-8').strip())
            stl = str(tds[25].get_text().encode('utf-8').strip())
            blk = str(tds[26].get_text().encode('utf-8').strip())
            fouls = str(tds[27].get_text().encode('utf-8').strip())
            dbldbl = str(tds[28].get_text().encode('utf-8').strip())
            trpdbl = str(tds[29].get_text().encode('utf-8').strip())
            indstats = [player_id, name, team, team_name, jersey, year, pos, height, played, started, minutes, fgm, fga, fgpct, three_fgm, three_fga, three_fgpct, ft, fta, ftpct, pts, ptsavg, offreb, defreb, totreb, rebavg, ast, to, stl, blk, fouls, dbldbl, trpdbl]
            player_list.append(indstats)
            if (scrapersettings.summary_players == 1):
                writeline = ""
                for item in indstats:
                    writeline += str(item) + "\t"
                writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                summary_player_data_w.writelines(writeline)


        # Get Team Data
        team_tds = stat_grid[0].find('tfoot').findAll('tr')[1].findAll('td')
        team_minutes = str(team_tds[7].get_text().encode('utf-8').strip())
        team_fgm = str(team_tds[8].get_text().encode('utf-8').strip())    
        team_fga = str(team_tds[9].get_text().encode('utf-8').strip())    
        team_fgpct = str(team_tds[10].get_text().encode('utf-8').strip()) 
        team_three_fgm = str(team_tds[11].get_text().encode('utf-8').strip())
        team_three_fga = str(team_tds[12].get_text().encode('utf-8').strip())
        team_three_fgpct = str(team_tds[13].get_text().encode('utf-8').strip())
        team_ft = str(team_tds[14].get_text().encode('utf-8').strip())    
        team_fta = str(team_tds[15].get_text().encode('utf-8').strip())   
        team_ftpct = str(team_tds[16].get_text().encode('utf-8').strip()) 
        team_pts = str(team_tds[17].get_text().encode('utf-8').strip())   
        team_ptsavg = str(team_tds[18].get_text().encode('utf-8').strip())
        team_offreb = str(team_tds[19].get_text().encode('utf-8').strip())
        team_defreb = str(team_tds[20].get_text().encode('utf-8').strip())
        team_totreb = str(team_tds[21].get_text().encode('utf-8').strip())
        team_rebavg = str(team_tds[22].get_text().encode('utf-8').strip())
        team_ast = str(team_tds[23].get_text().encode('utf-8').strip())   
        team_to = str(team_tds[24].get_text().encode('utf-8').strip())    
        team_stl = str(team_tds[25].get_text().encode('utf-8').strip())   
        team_blk = str(team_tds[26].get_text().encode('utf-8').strip())   
        team_fouls = str(team_tds[27].get_text().encode('utf-8').strip()) 
        team_dbldbl = str(team_tds[28].get_text().encode('utf-8').strip())
        team_trpdbl = str(team_tds[29].get_text().encode('utf-8').strip())
        team_stats = [team_minutes, team_fgm, team_fga, team_fgpct, team_three_fgm, team_three_fga, team_three_fgpct, team_ft, team_fta, team_ftpct, team_pts, team_ptsavg, team_offreb, team_defreb, team_totreb, team_rebavg, team_ast, team_to, team_stl, team_blk, team_fouls, team_dbldbl, team_trpdbl]

        # Get Opposing Team Data
        opp_team_tds = stat_grid[0].find('tfoot').findAll('tr')[2].findAll('td')
        opp_team_minutes = str(opp_team_tds[7].get_text().encode('utf-8').strip())
        opp_team_fgm = str(opp_team_tds[8].get_text().encode('utf-8').strip())    
        opp_team_fga = str(opp_team_tds[9].get_text().encode('utf-8').strip())    
        opp_team_fgpct = str(opp_team_tds[10].get_text().encode('utf-8').strip()) 
        opp_team_three_fgm = str(opp_team_tds[11].get_text().encode('utf-8').strip())
        opp_team_three_fga = str(opp_team_tds[12].get_text().encode('utf-8').strip())
        opp_team_three_fgpct = str(opp_team_tds[13].get_text().encode('utf-8').strip())
        opp_team_ft = str(opp_team_tds[14].get_text().encode('utf-8').strip())    
        opp_team_fta = str(opp_team_tds[15].get_text().encode('utf-8').strip())   
        opp_team_ftpct = str(opp_team_tds[16].get_text().encode('utf-8').strip()) 
        opp_team_pts = str(opp_team_tds[17].get_text().encode('utf-8').strip())   
        opp_team_ptsavg = str(opp_team_tds[18].get_text().encode('utf-8').strip())
        opp_team_offreb = str(opp_team_tds[19].get_text().encode('utf-8').strip())
        opp_team_defreb = str(opp_team_tds[20].get_text().encode('utf-8').strip())
        opp_team_totreb = str(opp_team_tds[21].get_text().encode('utf-8').strip())
        opp_team_rebavg = str(opp_team_tds[22].get_text().encode('utf-8').strip())
        opp_team_ast = str(opp_team_tds[23].get_text().encode('utf-8').strip())   
        opp_team_to = str(opp_team_tds[24].get_text().encode('utf-8').strip())    
        opp_team_stl = str(opp_team_tds[25].get_text().encode('utf-8').strip())   
        opp_team_blk = str(opp_team_tds[26].get_text().encode('utf-8').strip())   
        opp_team_fouls = str(opp_team_tds[27].get_text().encode('utf-8').strip()) 
        opp_team_dbldbl = str(opp_team_tds[28].get_text().encode('utf-8').strip())
        opp_team_trpdbl = str(opp_team_tds[29].get_text().encode('utf-8').strip())
        opp_team_stats = [opp_team_minutes, opp_team_fgm, opp_team_fga, opp_team_fgpct, opp_team_three_fgm, opp_team_three_fga, opp_team_three_fgpct, opp_team_ft, opp_team_fta, opp_team_ftpct, opp_team_pts, opp_team_ptsavg, opp_team_offreb, opp_team_defreb, opp_team_totreb, opp_team_rebavg, opp_team_ast, opp_team_to, opp_team_stl, opp_team_blk, opp_team_fouls, opp_team_dbldbl, opp_team_trpdbl]

        team_stats_total = [team, team_name] + team_stats + opp_team_stats
        if (scrapersettings.summary_teams == 1):
            writeline = ""
            for item in team_stats_total:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            summary_team_data_w.writelines(writeline)
    print "Successfully generated player mappings and/or summary data for players and/or summary data for teams"


if (scrapersettings.map_players == 1):
    player_dict = dict([(case[0], (case[1:])) for case in player_list]) # Create a dictionary from our list so we don't have any duplicate entries
    for item in player_dict: # For each item on that list
        player_mappingfile_w.writelines(str(item) + "\t" + player_dict[item][1] + "\t" + player_dict[item][0] + "\n")