# Polls2k11 - Get the latest polls for the Portuguese legislative election, 2011 #

## What's this? ##

Wikipedia has a pretty nice page showing opinion polls data relating
to the 2011 Portuguese legislative election. I had some ideas to use
that information but I need that information structured in a decent
format.

I built a script to access wikipedia and convert that information to
JSON. I made this public so everyone can use and create nice apps that
use that information.

## How to use ##

### Host it yourself ###

You can install this script and host it yourself, please do!

### Use http://polls.simaomata.com ###

You can also use my installation at http://polls.simaomata.com

The following endpoints are available:

    * http://polls.simaomata.com/all - Returns latest known
      information about all 2011 polls

    * http://polls.simaomata.com/latest - Returns information about
      the most recent poll

Endpoints are only updated once a day.

This can't be used in the client side, I am working on a solution to
provide these endpoints using JSONP so they can used on the client
side.


## Examples ##

### All ###


### Latest ###


## Please get inspired ##

There are so many things everyone can do with this information, you
just need to access these endpoints.

GO BUILD SOMETHING! No excuses.


## License ##




TODO:

Fazer um index para polls.simaomata.com
Party names infered from the data
Deploy
Deploy to github
Start a javascript client (Will have to serve it as jsonp, or serve it
in the same place, but I need jsonp for other people, probably can use
bottle)
