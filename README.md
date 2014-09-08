Screlp
======

## Synopsis

**Screlp** is a tool that queries the Yelp API and returns the results as a CSV file. It can take a single query and turn it into multiple, smaller-scale queries. In this way, it can retrieve more results than the standard Yelp API will allow. 

## Installation

To get started, you'll want to ensure all your dependencies are installed. The script `install_dependencies.sh` can handle this for you, but you will need to have root privileges.

One module, `pygmaps`, requires a pair of pip installation tags that allow for unverified, external modules to be installed. I've not seen any reason to believe that `pygmaps` is in any way malicious, rather that is just not hosted on PyPi. That said, all pygmaps does is generate HTML maps of the coordinates searched for in your query, so you're welcome to simply delete any references of it. Principally, in `screlp.py`, you'd want to eliminate the line that calls the function `create_search_map`

## Usage Example

    $ python3 screlp.py -a="603 Red River St. Austin, TX 78798" -t="pizza" -d=2 -r=2

## Command Line Arguments

- -a/--address: An address field. Used by pygeocoder module to retrieve decimal degrees coordinates for a given address.
- -t/--term: Search term. Implemented in the API URL construction as a search parameter.
- -r/--radius: Search radius. Used to generate multiple coordinates on the map and to limit results from a query.
- -d/--density: Coordinate grid density. Number provided is one greater than the number of points generated between the origin coordinate and the outer bounds coordinates. In the calculation of the number of coordinate points necessary to generate, it is the x in f(x) = (1+2x)²
