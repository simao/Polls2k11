# Polls2k11 - Get the latest polls for the Portuguese legislative election, 2011 #

## What's this? ##

Polls2k11 provides the latest poll information for the Portuguese
legislative election 2011 in a machine readable format, currently JSON
with JSONP support.

Wikipedia provides a pretty nice page showing opinion polls data
relating to the 2011 Portuguese legislative elections. I had some
ideas to use that information but I need that information structured
in a decent format.

I built a script to get the data from Wikipedia and convert that
information to JSON. I made this public so everyone can use and create
nice apps.

## How to use ##

### Host it yourself ###

You can install this script and host it yourself, please do!

If you don't require JSONP, all you need to do is run polls.py every
time you need to update the data.

If you need JSONP, you can deploy a pollserver.py and use the
endpoints defined there.

### Use http://polls.simaomata.com ###

You can also use my installation at
[polls.simaomata.com](http://polls.simaomata.com)

The following endpoints are available:

* [http://polls.simaomata.com/all](http://polls.simaomata.com/all) -
  Returns latest known information about all 2011 polls

*  [http://polls.simaomata.com/latest](http://polls.simaomata.com/latest) - Returns information about the most recent poll

All information provided by these endpoints is updated once a day.

All information can be obtained from a browser using JSONP. If you
pass a GET parameter named "jsonp=callbackName", the response will be
the following:

	callbackName(pollData);

Check the example below for more information on this.

## Example ##
### Using jQuery to get JSONP data ###

An example is provided in jsonp_example.html. This examples fetches
data from /all using JSONP and jQuery and displays the result in a
simple manner.

If you want to use the /latest endpoint from a browser, you can use
/latest?jsonp=mycallback. This endpoint will return the following
response:

	mycallback({
	    "date": "8-10 April",
	    "source": {
	        "href": "http://www.tvi24.iol.pt/politica/sondagem-psd-ps-eleicoes-intercampos-tvi24/1245972-4072.html",
	        "name": "INTERCAMPUS"
	    },
	    "parties": {
	        "Lead": "5.6",
	        "Others / undecided": "3.1",
	        "Socialist": "33.1",
	        "People's Party": "9.4",
	        "Green-Communist": "8.1",
	        "Social Democratic": "38.7",
	        "Left Bloc": "7.6"
	    }
	});

## Get Inspired ##

There are so many things everyone can do with this information, it's
so freakin easy to use it!

GO BUILD SOMETHING! No excuses.


## License ##

Copyright (C) 2011 by Simão Mata

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
