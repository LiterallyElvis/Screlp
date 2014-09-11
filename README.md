Screlp
======

## Synopsis

**Screlp** is a tool that queries the Yelp API and returns the results as a CSV file. It can take a single query and turn it into multiple, smaller-scale queries. In this way, it can retrieve more results than the standard Yelp API will allow.

## Setup

To get started, you'll want to ensure all your dependencies are installed by running the command `pip3 install -r requirements.txt`.

Once you've gotten your modules installed, you'll need to set up your yelp.creds file. The file is arranged so that you just copy paste the values from the Yelp API page in the order that they appear. For example, this is how the file should look with made-up values:

> Consumer Key = BLAHBLAHBLAHBLAH

> Consumer Secret = YARFYARFYARFYARF

> Token = MURRMURRMURRMURR

> Token Secret = BREEBREEBREEBREE

## Usage Example

    $ python3 screlp.py -a="603 Red River St. Austin, TX 78701" -t="pizza" -r=2 -d=3

## Command Line Arguments

- -a/--address: An address field. Used by pygeocoder module to retrieve decimal degrees coordinates for a given address.
- -t/--term: Search term. Implemented in the API URL construction as a search parameter.
- -r/--radius: Search radius. Used to generate multiple coordinates on the map and to limit results from a query.
- -d/--density: Coordinate grid density. Number provided is one greater than the number of points generated between the origin coordinate and the outer bounds coordinates. In the calculation of the number of coordinate points necessary to generate, it is the x in f(x) = (1+2x)²
- -c/--category: Category filter. Limits Yelp search results to within a cerrtain business category. Tricky to use properly, has to be taken from a list found here: http://www.yelp.com/developers/documentation/v2/all_category_list
