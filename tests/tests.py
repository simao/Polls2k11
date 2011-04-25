# -*- coding: utf-8 -*-
import os
import urllib2

import unittest
import simplejson as json
import polls
from codecs import open

LATEST_TEMP_FILE = "tests/latest_temp.json"
__author__ = 'Simao Mata'

class TestPolls(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        self.latest_poll = {
            "date" : u"8-10 April",
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
            }
        }


    def tearDown(self):
        if os.path.exists(LATEST_TEMP_FILE):
            os.unlink(LATEST_TEMP_FILE)

    def test_latest_main(self):
        self.monkey_patch_urlopen("http://localhost/wikipediapolls")

        polls.main("http://localhost/wikipediapolls", LATEST_TEMP_FILE, "tests/all_temp.json")

        with open(LATEST_TEMP_FILE, 'r') as fd:
            latest_poll = json.load(fd)

        self.assertDictEqual(self.latest_poll, latest_poll)

    def test_get_newest_poll(self):
        file_path = "tests/resources/full.html"

        with open(file_path, 'r', 'utf-8') as fd:
            poll_stats = polls.get_poll_newest(fd)

        self.assertDictEqual(self.latest_poll, poll_stats)


    def monkey_patch_urlopen(self, expected_url):
        '''
        Substitute urllib2.urlopen by a custom function that simple checks that the url is equal to expected_url
        and returns the content of the resources/full.html file
        '''
        #noinspection PyUnusedLocal
        def monkey_url_open(request, *args, **kwargs):
            self.assertEquals(expected_url, request.get_full_url())
            return open('tests/resources/full.html')
        urllib2.urlopen = monkey_url_open

    def test_get_newest_from_url(self):
        self.monkey_patch_urlopen("http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011")

        poll_stats = polls.get_poll_newest_from_url("http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011")
        self.assertDictEqual(self.latest_poll, poll_stats)

