NCAA Basketball Stats Scraper
=============================
Author: Rodrigo Zamith
Version: 1.0
By: Rodrigo Zamith


Usage
-----
First, edit the scraper settings in [scrapersettings.py]. In particular, be sure to change the two variables at the top, [academic_year] and [year_index], using the information provided in that file. You can also set what kind of data you'd like saved, and where you'd like it saved.

Then, execute either [ncaab_stats_scraper.sh] or [ncaab_stats_scraper.bat], depending on your operating system. Alternatively, you can just execute the python files, preferably in this order:
- create_team_mappings.py
- create_schedule_mappings.py
- create_player_mappings_and_agg_stats.py
- create_ind_stats.py


Requirements
------------
This script requires Python, as well as the urllib2 and BeautifulSoup libraries.


License
--------
This script is licensed under the Mozilla Public License Version 2.0 (see LICENSE file in root folder). TL;DR: feel free to use it commercially, modify it, and distribute it, provided you disclose both the source code and any moditations you make to it.