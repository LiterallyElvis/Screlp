"""
Screlp is an augmentation of the Yelp API. It takes a number of command-line
variables and uses them to generate a grid of coordinates. That list of
coordinates is used to make successive queries for the same information, and
all of the subsequent results are added to a giant list that is exported to CSV.
"""

import argparse
import src.geog as geog
import src.parse as parse
import src.files as files
import time


def argument_setup():
    """
    Sets up command-line arguments. The arguments are:

    Term: a search term to pass to the query URL. This is comparable to
          terms you would enter into the search field on the full Yelp
          website

    Address: an address used as the origin point for the coordinate generation.
             Address given is mandatory and sent to the pygeoparser module. The
             module then sends that address to the Google Maps API and
             retrieves a set of latitude and longitude points in return.

    Category: a category to filter results through. If you just search for
              something like "pizza", Yelp will return a whole slew of things
              that may or may not actually be wholly dedicated to pizza. It
              will return not only places like Roppolo's, but it will also
              return H-E-B. See this url for the full list of valid category
              filters:
              http://www.yelp.com/developers/documentation/v2/all_category_list

    Radius: a radius to limit the search results to. Currently, this sets the
            same radius for all coordinate queries. Eventually it will be used
            as the radius for coordinate generation and, in conjunction with
            the density, to calculate the radius for all points.

    Density: the grid density. Currently this is one greater than the number
             of points placed between the origin point and the outer bound
             points. For example, if the density is set to 1 (the default),
             there will be one point between the outer bounds and the origin
             point when the coordinate grid is generated.
    """
    parser = argparse.ArgumentParser(description="Fetches Yelp results.")
    parser.add_argument("-t", "--term", action="store", dest="term",
                        help="Specific term to search Yelp for")
    parser.add_argument("-a", "--address", action="store", dest="address",
                        required=True, help="Address to base query upon")
    parser.add_argument("-c", "--category", action="store", dest="category",
                        help="Category to limit results within")
    parser.add_argument("-r", "--radius", action="store", dest="radius",
                        default=1, help="Radius in miles from origin.")
    parser.add_argument("-d", "--density", action="store", dest="density",
                        default=1, help="Grid density")

    parser = parser.parse_args()

    return parser


def main():
    """
    This is the main order of operations. The program starts by setting a time
    variable to keep track of how long the script takes to run.

    The program then sets up its command line arguments, and passes them to the
    get_geocode function. That returns a pair of coordinates called origin,
    which is used to generate a grid of coordinates. These coordinates are made
    into a map to detail what points were used in the search. They are then
    used to make a series of queries against the Yelp API.

    Those results are returned as a list that is then passed to a file
    writing procedure. If you'd like to have the raw results show up, you can
    add the line "files.write_raw_results(yelp_results, args)" below the line
    that says "files.write_csv_file(yelp_results)."

    The program ends by telling you how long your query took to process.
    """
    start = time.time()
    args = argument_setup()
    origin = geog.get_geocode(args)
    results = geog.generate_coords(origin, int(args.density), int(args.radius))
    yelp_results = parse.scrape_yelp(args, results)
    files.create_search_map(origin, results, True, int(args.radius))
    files.write_csv_file(yelp_results)
    print("Execution time: {:.2f}{}".format((time.time() - start), " seconds"))

main()
