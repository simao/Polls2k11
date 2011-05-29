# -*- coding: utf-8 -*-
import codecs
from bottle import static_file, response, get, request
import bottle
import polls

__author__ = 'Simão Mata'

STATIC_FILES_DIR = "static/"

ALL_POLLS_FILE = polls.ALL_POLLS_FILE
LATEST_POLL_FILE = polls.LATEST_POLL_FILE
DEFAULT_CONTENT_TYPE = "application/javascript; charset=UTF8"

@get('/')
def get_index():
    return static_file("index.html", root=STATIC_FILES_DIR, mimetype="text/html; charset=UTF8")

@get('/all')
def get_all():
    jsonp_func = request.GET.get('jsonp', None)
    return _get_poll_file(ALL_POLLS_FILE, jsonp_func)

@get('/latest')
def get_all():
    jsonp_func = request.GET.get('jsonp', None)
    return _get_poll_file(LATEST_POLL_FILE, jsonp_func)

def _get_poll_file(path, jsonp_func=None):
    http_response = static_file(path, root='./', mimetype=DEFAULT_CONTENT_TYPE)
    if http_response.status != 200:
        return http_response
    elif jsonp_func:
        with codecs.open(path, 'r', 'utf-8') as fd:
            all_polls = fd.read()
            response.content_type = DEFAULT_CONTENT_TYPE

            return "%s(%s);" % (jsonp_func, all_polls)
    else:
        return http_response


if __name__ == "__main__":
    bottle.debug(True)
    bottle.run(reloader=True)


