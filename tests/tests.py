# -*- coding: utf-8 -*-
import urllib2

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import polls
from codecs import open

__author__ = 'Simao Mata'

class TestPolls(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        self.latest_poll = {
            "date" : u"8–10 April",
            "source" : {
                "href" : u"http://www.tvi24.iol.pt/politica/sondagem-psd-ps-eleicoes-intercampos-tvi24/1245972-4072.html",
                "name" : u"INTERCAMPUS",
            },
            "parties" : {
                "Socialist" : u"33.1",
                "Social Democratic" : u"38.7",
                "People's Party" : u"9.4",
                "Left Bloc" : u"7.6",
                "Green-Communist" : u"8.1",
                "Others / undecided" : u"3.1",
                "Lead" : u"5.6",
            }
        }



    def test_get_newest_poll(self):
        file_path = "tests/resources/full.html"

        with open(file_path, 'r', 'utf-8') as fd:
            poll_stats = polls.get_poll_newest(fd)

        self.assertDictEqual(self.latest_poll, poll_stats)


    @unittest.skip("Dont mess with wikipedia")
    def test_get_newest_from_url(self):
        poll_stats = polls.get_poll_newest_from_url("http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011")
        self.assertDictEqual(self.latest_poll, poll_stats)
