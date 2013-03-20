#!/usr/bin/python
##############################################################
# Program name: NCAA Basketball Stats Scraper (Functions Module)
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

import cookielib
import urllib
import urllib2
import re
import scrapersettings

### Retry Decorator code taken from the SaltyCrane Blog (http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/)
import time
from functools import wraps


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry



### Define our functions
def create_cookie():
    # Create a cookie handler, if necessary
    cookie_jar = cookielib.LWPCookieJar()
    cookie = urllib2.HTTPCookieProcessor(cookie_jar)
    
    # Create an urllib2 opener() using our cookie jar
    opencookies = urllib2.build_opener(cookie)
    return(opencookies)

@retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    # Create a cookie jar
    cookiejar = create_cookie()
    # Create the HTTP request
    req = urllib2.Request(url, urllib.urlencode(params), http_header)
    
    # Submit the request
    res = cookiejar.open(req)
    data = res.read()
    return(data)

def get_team_mappings():
    team_map = open(scrapersettings.team_mappingfile, "rb")
    team_map = team_map.readlines()[1:]
    team_map = dict([(var.split("\t")[0], (var.split("\t")[1], var.split("\t")[2].strip("\n"))) for var in team_map])
    return(team_map)

def get_game_mappings():
    game_map = open(scrapersettings.schedule_mappingfile, "rb")
    game_map = game_map.readlines()[1:]
    game_map = dict([(var.split("\t")[0], (var.split("\t")[1], var.split("\t")[2], var.split("\t")[3], var.split("\t")[4], var.split("\t")[5].strip("\n"))) for var in game_map])
    return(game_map)