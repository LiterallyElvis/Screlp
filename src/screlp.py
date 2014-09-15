import argparse
import geog
import parse
import files
import time


def argument_setup():
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

    return parser.parse_args()


def main():
    start = time.time()
    args = argument_setup()
    origin = geog.get_geocode(args)
    results = geog.generate_coords(origin, int(args.density), int(args.radius))
    geog.create_search_map(origin, results, True, int(args.radius))
    yelp_results = parse.scrape_yelp(args, results)
    files.write_csv_file(yelp_results)
    files.write_raw_result(yelp_results, args)
    print("Execution time: {:.2f}{}".format((time.time() - start), " seconds"))

main()
