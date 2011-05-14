# -*- coding: utf-8 -*-
import os
import urllib2

import unittest
import simplejson as json
import polls
from codecs import open

TEST_WIKIPEDIA_PAGE = 'tests/resources/full.html'
LATEST_TEMP_FILE = "tests/latest_temp.json"
__author__ = 'Simao Mata'

class TestPolls(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        self.latest_poll = {
            "date" : u"7-12 May",
            "source" : {
                "href" : u"http://www.publico.pt/Pol%C3%ADtica/ps-passa-psd-e-cds-dispara-para-os-134_1494074?all=1",
                "name" : u"INTERCAMPUS",
            },
            "parties" : {
                u"Socialist" : u"36.8",
                u"Social Democratic" : u"33.9",
                u"People's Party" : u"13.4",
                u"Left Bloc" : u"6.0",
                u"Green-Communist" : u"7.4",
                u"Others / undecided" : u"2.4",
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
        file_path = TEST_WIKIPEDIA_PAGE

        with open(file_path, 'r', 'utf-8') as fd:
            poll_stats = polls.get_poll_newest(fd)

        self.assertDictEqual(self.latest_poll, poll_stats)


    def monkey_patch_urlopen(self, expected_url):
        '''
        Substitute urllib2.urlopen by a custom function that checks that the url is equal to expected_url
        and returns the content of the resources/full.html file

        TODO: This method of testing assumes the code will use urlopen, we shouldn't care about what lib is being
        used to get the url. We should setup a small stub http server to serve the page
        '''
        #noinspection PyUnusedLocal
        def monkey_url_open(request, *args, **kwargs):
            self.assertEquals(expected_url, request.get_full_url())
            return open(TEST_WIKIPEDIA_PAGE)
        urllib2.urlopen = monkey_url_open

    def test_get_newest_from_url(self):
        self.monkey_patch_urlopen("http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011")

        poll_stats = polls.get_poll_newest_from_url("http://en.wikipedia.org/wiki/Portuguese_legislative_election,_2011")
        self.assertDictEqual(self.latest_poll, poll_stats)

