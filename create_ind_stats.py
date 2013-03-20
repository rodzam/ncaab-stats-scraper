#!/usr/bin/python
##############################################################
# Program name: NCAA Basketball Stats Scraper (Individual Stats Module)
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

if (scrapersettings.ind_game_stats == 1):
    # Create the file headings
    game_data_w = open(scrapersettings.game_data, "w")
    game_data_w.writelines("game_id\tgame_date\taway_team_id\taway_team_name\taway_team_minutes\taway_team_fgm\taway_team_fga\taway_team_three_fgm\taway_team_three_fga\taway_team_ft\taway_team_fta\taway_team_pts\taway_team_offreb\taway_team_defreb\taway_team_totreb\taway_team_ast\taway_team_to\taway_team_stl\taway_team_blk\taway_team_fouls\thome_team_id\thome_team_name\thome_team_minutes\thome_team_fgm\thome_team_fga\thome_team_three_fgm\thome_team_three_fga\thome_team_ft\thome_team_fta\thome_team_pts\thome_team_offreb\thome_team_defreb\thome_team_totreb\thome_team_ast\thome_team_to\thome_team_stl\thome_team_blk\thome_team_fouls\tneutral_site\n")

if (scrapersettings.ind_player_stats == 1):
    # Create the file headings
    player_data_w = open(scrapersettings.player_data, "w")
    player_data_w.writelines("player_id\tplayer_name\tteam_id\tteam_name\tgame\tpos\tminutes\tfgm\tfga\tthree_fgm\tthree_fga\tft\tfta\tpts\toffreb\tdefreb\ttotreb\tast\tto\tstl\tblk\tfouls\tgame_date\tneutral_site\n")

if (scrapersettings.ind_team_stats == 1):
    # Create the file headings
    team_data_w = open(scrapersettings.team_data, "w")
    team_data_w.writelines("game_id\tgame_date\tsite\tteam_id\tteam_name\tteam_minutes\tteam_fgm\tteam_fga\tteam_three_fgm\tteam_three_fga\tteam_ft\tteam_fta\tteam_pts\tteam_offreb\tteam_defreb\tteam_totreb\tteam_ast\tteam_to\tteam_stl\tteam_blk\tteam_fouls\n")


if (scrapersettings.ind_game_stats == 1) or (scrapersettings.ind_player_stats == 1) or (scrapersettings.ind_team_stats == 1):
    print "Generating individual statistics for players and/or teams"
    
    # Grab data
    # Parse our mappings file to get our list of teams
    team_mapping = scraperfunctions.get_team_mappings()

    # Parse our schedule file to get a list of games
    game_mapping = scraperfunctions.get_game_mappings()

    # Parse the stats tables
    team_stats_total = [] # Create an empty list for storing the team stats
    alphanum = re.compile(r'[^\w\s:]+')
    for value, game in enumerate(game_mapping): # For each game in our dictionary
        if scrapersettings.debugmode == 1: print "Processing game " + str(game) + " (" + str(value+1) + " of " + str(len(game_mapping)) + ")"
        game_url = game_mapping[game][4]
        try:
            game_page_data = scraperfunctions.grabber(game_url, scrapersettings.params, scrapersettings.http_header) # Grab the main page for each team
        except:
            print "Error getting data. Moving on to next game."
            continue
        game_page_data_soup = BeautifulSoup(game_page_data)
        neutral = game_mapping[game][3]
        tables = game_page_data_soup.findAll('table', class_='mytable')
        headertable = tables[0]
        awaystats = tables[1]
        homestats = tables[2]

        # Get Participants
        away_team_header = headertable.findAll('tr')[1]
        tds = away_team_header.findAll('td')
        try:
            away_team =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
        except:
            away_team = 0
        try:
            away_team_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
        except:
            try:
                away_team_name = str(tds[0].get_text().encode('utf-8').strip())
            except:
                away_team_name = "Not Available"
        home_team_header = headertable.findAll('tr')[2]
        tds = home_team_header.findAll('td')
        try:
            home_team =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
        except:
            home_team = 0
        try:
            home_team_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
        except:
            try:
                home_team_name = str(tds[0].get_text().encode('utf-8').strip())
            except:
                home_team_name = "Not Available"

        # Get date
        date_locator = re.compile(r'Game Date:')
        date_pattern = re.compile(r'\d+/\d+/\d+')
        try:
            gamedate = re.search(date_pattern, game_page_data_soup.find('td', text=date_locator).find_next('td').get_text()).group(0)
        except:
            gamedate = "ERROR!"

        # Get Away Team Data
        for rowno, row in enumerate(awaystats.findAll('tr', class_='smtext')[:-1]):
            tds = row.findAll('td')
            try:
                player_id =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
            except:
                player_id = 0
            try:
                player_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
            except:
                try:
                    player_name = str(tds[0].get_text().encode('utf-8').strip())
                except:
                    player_name = "Not Available"
            try:
                pos = str(tds[1].get_text().encode('utf-8').strip())
                pos = alphanum.sub('', pos)
            except:
                pos = "ERROR!"
            try:
                minutes = str(tds[2].get_text().encode('utf-8').strip())
                minutes = alphanum.sub('', minutes)
            except:
                minutes = "ERROR!"
            try:
                fgm = str(tds[3].get_text().encode('utf-8').strip())
                fgm = alphanum.sub('', fgm)
            except:
                fgm = "ERROR!"
            try:
                fga = str(tds[4].get_text().encode('utf-8').strip())
                fga = alphanum.sub('', fga)
            except:
                fga = "ERROR!"
            try:
                three_fgm = str(tds[5].get_text().encode('utf-8').strip())
                three_fgm = alphanum.sub('', three_fgm)
            except:
                three_fgm = "ERROR!"
            try:
                three_fga = str(tds[6].get_text().encode('utf-8').strip())
                three_fga = alphanum.sub('', three_fga)
            except:
                three_fga = "ERROR!"
            try:
                ft = str(tds[7].get_text().encode('utf-8').strip())
                ft = alphanum.sub('', ft)
            except:
                ft = "ERROR!"
            try:
                fta = str(tds[8].get_text().encode('utf-8').strip())
                fta = alphanum.sub('', fta)
            except:
                fta = "ERROR!"
            try:
                pts = str(tds[9].get_text().encode('utf-8').strip())
                pts = alphanum.sub('', pts)
            except:
                pts = "ERROR!"
            try:
                offreb = str(tds[10].get_text().encode('utf-8').strip())
                offreb = alphanum.sub('', offreb)
            except:
                offreb = "ERROR!"
            try:
                defreb = str(tds[11].get_text().encode('utf-8').strip())
                defreb = alphanum.sub('', defreb)
            except:
                defreb = "ERROR!"
            try:
                totreb = str(tds[12].get_text().encode('utf-8').strip())
                totreb = alphanum.sub('', totreb)
            except:
                totreb = "ERROR!"
            try:
                ast = str(tds[13].get_text().encode('utf-8').strip())
                ast = alphanum.sub('', ast)
            except:
                ast = "ERROR!"
            try:
                to = str(tds[14].get_text().encode('utf-8').strip())
                to = alphanum.sub('', to)
            except:
                to = "ERROR!"
            try:
                stl = str(tds[15].get_text().encode('utf-8').strip())
                stl = alphanum.sub('', stl)
            except:
                stl = "ERROR!"
            try:
                blk = str(tds[16].get_text().encode('utf-8').strip())
                blk = alphanum.sub('', blk)
            except:
                blk = "ERROR!"
            try:
                fouls = str(tds[17].get_text().encode('utf-8').strip())
                fouls = alphanum.sub('', fouls)
            except:
                fouls = "ERROR!"
            ind_stats = [player_id, player_name, away_team, away_team_name, game, pos, minutes, fgm, fga, three_fgm, three_fga, ft, fta, pts, offreb, defreb, totreb, ast, to, stl, blk, fouls]
            if (scrapersettings.ind_player_stats == 1):
                writeline = ""
                for item in ind_stats:
                    writeline += str(item) + "\t"
                writeline += str(gamedate) + "\t" + str(neutral)
                #writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                player_data_w.writelines(writeline)

        # Get Home Team Data
        for rowno, row in enumerate(homestats.findAll('tr', class_='smtext')[:-1]):
            tds = row.findAll('td')
            try:
                player_id =  str(tds[0].find('a').get('href').split('=')[-1].encode('utf-8').strip())
            except:
                player_id = 0
            try:
                player_name =  str(tds[0].find('a').get_text().encode('utf-8').strip())
            except:
                try:
                    player_name = str(tds[0].get_text().encode('utf-8').strip())
                except:
                    player_name = "Not Available"
            try:
                pos = str(tds[1].get_text().encode('utf-8').strip())
                pos = alphanum.sub('', pos)
            except:
                pos = "ERROR!"
            try:
                minutes = str(tds[2].get_text().encode('utf-8').strip())
                minutes = alphanum.sub('', minutes)
            except:
                minutes = "ERROR!"
            try:
                fgm = str(tds[3].get_text().encode('utf-8').strip())
                fgm = alphanum.sub('', fgm)
            except:
                fgm = "ERROR!"
            try:
                fga = str(tds[4].get_text().encode('utf-8').strip())
                fga = alphanum.sub('', fga)
            except:
                fga = "ERROR!"
            try:
                three_fgm = str(tds[5].get_text().encode('utf-8').strip())
                three_fgm = alphanum.sub('', three_fgm)
            except:
                three_fgm = "ERROR!"
            try:
                three_fga = str(tds[6].get_text().encode('utf-8').strip())
                three_fga = alphanum.sub('', three_fga)
            except:
                three_fga = "ERROR!"
            try:
                ft = str(tds[7].get_text().encode('utf-8').strip())
                ft = alphanum.sub('', ft)
            except:
                ft = "ERROR!"
            try:
                fta = str(tds[8].get_text().encode('utf-8').strip())
                fta = alphanum.sub('', fta)
            except:
                fta = "ERROR!"
            try:
                pts = str(tds[9].get_text().encode('utf-8').strip())
                pts = alphanum.sub('', pts)
            except:
                pts = "ERROR!"
            try:
                offreb = str(tds[10].get_text().encode('utf-8').strip())
                offreb = alphanum.sub('', offreb)
            except:
                offreb = "ERROR!"
            try:
                defreb = str(tds[11].get_text().encode('utf-8').strip())
                defreb = alphanum.sub('', defreb)
            except:
                defreb = "ERROR!"
            try:
                totreb = str(tds[12].get_text().encode('utf-8').strip())
                totreb = alphanum.sub('', totreb)
            except:
                totreb = "ERROR!"
            try:
                ast = str(tds[13].get_text().encode('utf-8').strip())
                ast = alphanum.sub('', ast)
            except:
                ast = "ERROR!"
            try:
                to = str(tds[14].get_text().encode('utf-8').strip())
                to = alphanum.sub('', to)
            except:
                to = "ERROR!"
            try:
                stl = str(tds[15].get_text().encode('utf-8').strip())
                stl = alphanum.sub('', stl)
            except:
                stl = "ERROR!"
            try:
                blk = str(tds[16].get_text().encode('utf-8').strip())
                blk = alphanum.sub('', blk)
            except:
                blk = "ERROR!"
            try:
                fouls = str(tds[17].get_text().encode('utf-8').strip())
                fouls = alphanum.sub('', fouls)
            except:
                fouls = "ERROR!"
            ind_stats = [player_id, player_name, home_team, home_team_name, game, pos, minutes, fgm, fga, three_fgm, three_fga, ft, fta, pts, offreb, defreb, totreb, ast, to, stl, blk, fouls]
            if (scrapersettings.ind_player_stats == 1):
                writeline = ""
                for item in ind_stats:
                    writeline += str(item) + "\t"
                writeline += str(gamedate) + "\t" + str(neutral)
                #writeline = re.sub('\t$', '', writeline)
                writeline += "\n"
                player_data_w.writelines(writeline)

        # Get Away Team Data
        away_results = awaystats.findAll('tr', class_='grey_heading')[-1:]
        tds = away_results[0].findAll('td')
        try:
            minutes = str(tds[2].get_text().encode('utf-8').strip())
            minutes = alphanum.sub('', minutes)
        except:
            minutes = "ERROR!"
        try:
            fgm = str(tds[3].get_text().encode('utf-8').strip())
            fgm = alphanum.sub('', fgm)
        except:
            fgm = "ERROR!"
        try:
            fga = str(tds[4].get_text().encode('utf-8').strip())
            fga = alphanum.sub('', fga)
        except:
            fga = "ERROR!"
        try:
            three_fgm = str(tds[5].get_text().encode('utf-8').strip())
            three_fgm = alphanum.sub('', three_fgm)
        except:
            three_fgm = "ERROR!"
        try:
            three_fga = str(tds[6].get_text().encode('utf-8').strip())
            three_fga = alphanum.sub('', three_fga)
        except:
            three_fga = "ERROR!"
        try:
            ft = str(tds[7].get_text().encode('utf-8').strip())
            ft = alphanum.sub('', ft)
        except:
            ft = "ERROR!"
        try:
            fta = str(tds[8].get_text().encode('utf-8').strip())
            fta = alphanum.sub('', fta)
        except:
            fta = "ERROR!"
        try:
            pts = str(tds[9].get_text().encode('utf-8').strip())
            pts = alphanum.sub('', pts)
        except:
            pts = "ERROR!"
        try:
            offreb = str(tds[10].get_text().encode('utf-8').strip())
            offreb = alphanum.sub('', offreb)
        except:
            offreb = "ERROR!"
        try:
            defreb = str(tds[11].get_text().encode('utf-8').strip())
            defreb = alphanum.sub('', defreb)
        except:
            defreb = "ERROR!"
        try:
            totreb = str(tds[12].get_text().encode('utf-8').strip())
            totreb = alphanum.sub('', totreb)
        except:
            totreb = "ERROR!"
        try:
            ast = str(tds[13].get_text().encode('utf-8').strip())
            ast = alphanum.sub('', ast)
        except:
            ast = "ERROR!"
        try:
            to = str(tds[14].get_text().encode('utf-8').strip())
            to = alphanum.sub('', to)
        except:
            to = "ERROR!"
        try:
            stl = str(tds[15].get_text().encode('utf-8').strip())
            stl = alphanum.sub('', stl)
        except:
            stl = "ERROR!"
        try:
            blk = str(tds[16].get_text().encode('utf-8').strip())
            blk = alphanum.sub('', blk)
        except:
            blk = "ERROR!"
        try:
            fouls = str(tds[17].get_text().encode('utf-8').strip())
            fouls = alphanum.sub('', fouls)
        except:
            fouls = "ERROR!"
        away_team_stats = [away_team, away_team_name, minutes, fgm, fga, three_fgm, three_fga, ft, fta, pts, offreb, defreb, totreb, ast, to, stl, blk, fouls]

        # Get Home Team Data
        home_results = homestats.findAll('tr', class_='grey_heading')[-1:]
        tds = home_results[0].findAll('td')
        try:
            minutes = str(tds[2].get_text().encode('utf-8').strip())
            minutes = alphanum.sub('', minutes)
        except:
            minutes = "ERROR!"
        try:
            fgm = str(tds[3].get_text().encode('utf-8').strip())
            fgm = alphanum.sub('', fgm)
        except:
            fgm = "ERROR!"
        try:
            fga = str(tds[4].get_text().encode('utf-8').strip())
            fga = alphanum.sub('', fga)
        except:
            fga = "ERROR!"
        try:
            three_fgm = str(tds[5].get_text().encode('utf-8').strip())
            three_fgm = alphanum.sub('', three_fgm)
        except:
            three_fgm = "ERROR!"
        try:
            three_fga = str(tds[6].get_text().encode('utf-8').strip())
            three_fga = alphanum.sub('', three_fga)
        except:
            three_fga = "ERROR!"
        try:
            ft = str(tds[7].get_text().encode('utf-8').strip())
            ft = alphanum.sub('', ft)
        except:
            ft = "ERROR!"
        try:
            fta = str(tds[8].get_text().encode('utf-8').strip())
            fta = alphanum.sub('', fta)
        except:
            fta = "ERROR!"
        try:
            pts = str(tds[9].get_text().encode('utf-8').strip())
            pts = alphanum.sub('', pts)
        except:
            pts = "ERROR!"
        try:
            offreb = str(tds[10].get_text().encode('utf-8').strip())
            offreb = alphanum.sub('', offreb)
        except:
            offreb = "ERROR!"
        try:
            defreb = str(tds[11].get_text().encode('utf-8').strip())
            defreb = alphanum.sub('', defreb)
        except:
            defreb = "ERROR!"
        try:
            totreb = str(tds[12].get_text().encode('utf-8').strip())
            totreb = alphanum.sub('', totreb)
        except:
            totreb = "ERROR!"
        try:
            ast = str(tds[13].get_text().encode('utf-8').strip())
            ast = alphanum.sub('', ast)
        except:
            ast = "ERROR!"
        try:
            to = str(tds[14].get_text().encode('utf-8').strip())
            to = alphanum.sub('', to)
        except:
            to = "ERROR!"
        try:
            stl = str(tds[15].get_text().encode('utf-8').strip())
            stl = alphanum.sub('', stl)
        except:
            stl = "ERROR!"
        try:
            blk = str(tds[16].get_text().encode('utf-8').strip())
            blk = alphanum.sub('', blk)
        except:
            blk = "ERROR!"
        try:
            fouls = str(tds[17].get_text().encode('utf-8').strip())
            fouls = alphanum.sub('', fouls)
        except:
            fouls = "ERROR!"
        home_team_stats = [home_team, home_team_name, minutes, fgm, fga, three_fgm, three_fga, ft, fta, pts, offreb, defreb, totreb, ast, to, stl, blk, fouls]

        total_team_stats = [game, gamedate] + away_team_stats + home_team_stats
        
        if (scrapersettings.ind_game_stats == 1):
            writeline = ""
            for item in total_team_stats:
                writeline += str(item) + "\t"
            writeline += str(neutral)
            #writeline = re.sub('\t$', '', writeline)            
            writeline += "\n"
            game_data_w.writelines(writeline)

        if (scrapersettings.ind_team_stats == 1):
            writeline = str(game) + "\t" + str(gamedate) + "\t"
            if neutral == "1":
                writeline += "Neutral" + "\t"
            else:
                writeline += "Away" + "\t"
            for item in away_team_stats:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            writeline += str(game) + "\t" + str(gamedate) + "\t"
            if neutral == "1":
                writeline += "Neutral" + "\t"
            else:
                writeline += "Home" + "\t"
            for item in home_team_stats:
                writeline += str(item) + "\t"
            writeline = re.sub('\t$', '', writeline)
            writeline += "\n"
            team_data_w.writelines(writeline)

    print "Successfully generated individual statistics for players and/or teams"