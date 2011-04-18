# -*- coding: utf-8 -*-
import urllib2
import simplejson as json
import codecs

__author__ = 'Simao Mata'

ALL_POLLS_FILE = "all_polls.json"
LATEST_POLL_FILE = "latest.json"

POLLS_URL = "http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011"

from beautifulsoup import BeautifulSoup

import logging

logging.basicConfig(level=logging.DEBUG)

_log = logging.getLogger(__name__)

def get_polls_all(fd, limit=None):
    """
    Scrape an file like object and return a list in which each element represents
    information about a poll
    """
    soup = BeautifulSoup(fd)

    tables = soup.findAll("table", { "class" : "wikitable sortable" })

    if len(tables) > 1: # TODO This can actually be handled checking for info inside each table
        raise Exception("Too many tables found")

    tr_lines = tables[0].findAll("tr")[1:]

    all_polls = []

    for poll in tr_lines:
        if limit and len(all_polls) >= limit:
            _log.debug("Stopped parsing. Already parsed until limit = %s" % limit)
            break

        cells = poll.findAll("td")

        if len(cells) != 9:
            _log.info("Stopping parsing. Line does not have 9 columns. We need 8 columns to parse stats.")
            break

        cells_t = [c.string.replace("%","") if c.string is not None else None for c in cells ]

        a_tag = cells[1].find('a')
        href = dict(a_tag.attrs)["href"]
        institute = a_tag.string

        all_polls.append({
                "date" : cells_t[0],
                "source" : {
                    "href" : href,
                    "name" : institute,
                },
                "parties" : { # TODO Parties names can be infered from the header
                    "Socialist" : cells_t[2],
                    "Social Democratic" : cells_t[3],
                    "People's Party" : cells_t[4],
                    "Left Bloc" : cells_t[5],
                    "Green-Communist" : cells_t[6],
                    "Others / undecided" : cells_t[7],
                    "Lead" : cells_t[8],
                }
            })

        _log.info("Parsed polls for %s" % cells_t[0])

    return all_polls

def get_poll_newest(fd):
    """
    Receive a file like object and read contents in order
    to return the latest available poll from the contents of
    the file like object
    """
    results = get_polls_all(fd, 1)
    return len(results) and results[0] or []

def get_poll_newest_from_url(url):
    results = get_polls_from_url(url, 1)
    return len(results) and results[0] or []

def get_polls_from_url(url, limit=None):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    return get_polls_all(response, limit=limit)

if __name__ == "__main__":
    _log.debug("Will parse last poll to %s" % ALL_POLLS_FILE)
    _log.debug("Will dump all polls to %s" % LATEST_POLL_FILE)

    all_polls = get_polls_from_url(POLLS_URL)

    with codecs.open(ALL_POLLS_FILE, 'w', 'UTF-8') as fd:
        json.dump(all_polls, fd, indent=4, ensure_ascii=False)

    if len(all_polls) > 0:
        with codecs.open(LATEST_POLL_FILE, 'w', 'UTF-8') as fd:
            json.dump(all_polls[0], fd, indent=4, ensure_ascii=False)
    else:
        _log.error("Could not parse polls. Not saving latest poll")

    _log.info("Finished.")


