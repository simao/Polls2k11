# -*- coding: utf-8 -*-
from itertools import izip
import urllib2
import simplejson as json
import codecs
from beautifulsoup import BeautifulSoup
import logging
import logging.handlers


__author__ = 'Simao Mata'

ALL_POLLS_FILE = "all_polls.json"
LATEST_POLL_FILE = "latest.json"

POLLS_URL = "http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011"

LOG_FORMAT = '[%(levelname).1s] [%(asctime)s] [%(name)s] %(message)s'
LOG_FILE = "polls.log"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

txt_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='D')
log_formatter = logging.Formatter(LOG_FORMAT)
txt_handler.setFormatter(log_formatter)
logging.getLogger(__name__).addHandler(txt_handler)

_log = logging.getLogger(__name__)

_clean_table = {
    "%" : "",
    u"–" : "-"
}

def _clean_data(data):
    """
    Changes data replacing all chars present in the keys of clean_table by the corresponding value
    and return the changed string.
    """
    for k, v in _clean_table.iteritems():
        data = data.replace(k, v)
    return data

def get_polls_all(fd, limit=None):
    """
    Scrape an file like object and return a list in which each element represents
    information about a poll
    """
    soup = BeautifulSoup(fd)

    tables = soup.findAll("table", { "class" : "wikitable sortable" })

    if len(tables) > 1: # TODO This can actually be handled checking for info inside each table
        raise Exception("Too many tables found")

    all_trs = tables[0].findAll("tr")
    tr_lines = all_trs[1:]

    # Find out parties names
    # All names are on the first line of the table
    # Search for font tags
    font_tags = all_trs[0].findAllNext("font")
    parties_names = [f.string for f in font_tags]

    all_polls = []
    # TODO Further asserts/verifies are needed to make sure we can use this table
    for poll in tr_lines:
        if limit and len(all_polls) >= limit:
            _log.debug("Stopped parsing. Already parsed until limit = %s" % limit)
            break

        cells = poll.findAll("td")

        if len(cells) != 9:
            _log.info("Stopping parsing. Line does not have 9 columns. We need 8 columns to parse stats.")
            break

        cells_t = [_clean_data(c.string) if c.string is not None else None for c in cells ]

        a_tag = cells[1].find('a')
        href = dict(a_tag.attrs)["href"]
        institute = a_tag.string

        current_poll_data = {
                "date" : _clean_data(cells_t[0]), # We actually handle this OK, but clients will probably have problems
                "source" : {
                    "href" : href,
                    "name" : institute,
                },
                "parties" : {}
            }

        current_poll_data["parties"].update((partie, cells_t[n]) for partie, n in izip(parties_names, range(2,8)))

        all_polls.append(current_poll_data)

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


def main():
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


if __name__ == "__main__":
    main()


