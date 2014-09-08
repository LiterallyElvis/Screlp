# -*- coding: utf-8 -*-
import argparse
import geog
import connect
import parse
import files

parser = argparse.ArgumentParser(description="Fetches Yelp results.")
parser.add_argument("-t", "--term", action="store", dest="term",
                    help="Category on yelp to search for")
parser.add_argument("-a", "--address", action="store", dest="address",
                    required=True, help="Address to base query upon")
parser.add_argument("-r", "--radius", action="store", dest="radius", default=1,
                    help="Radius in miles from origin coordinate.")
parser.add_argument("-d", "--density", action="store", dest="density",
                    default=1, help="Grid density")

args = parser.parse_args()

origin = geog.get_geocode(args)
results = geog.generate_coords(origin, int(args.density), int(args.radius))
geog.create_search_map(origin, results, True, int(args.radius))
yelp_results = parse.scrape_yelp(args, results)
yelp_results = parse.eliminate_duplicate_results(yelp_results)
files.write_csv_file(yelp_results)
files.write_raw_result(yelp_results, args)
