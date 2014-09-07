# -*- coding: utf-8 -*-
from pygeocoder import Geocoder
from requests_oauthlib import OAuth1Session
import argparse
import sys
import json
import math
import pygmaps
import csv

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
X_INCREMENT = .014474
Y_INCREMENT = .016761
items = []
gmap = pygmaps.maps(0.0, 0.0, 14)


class Business:
    """
    Business object to store desired data.

    Ultimately collected into a list of like objects for later comprehension.
    """
    def __init__(self):
        self.result_position = 0
        self.id = None
        self.name = None
        self.address = None
        self.city = None
        self.state = None
        self.zip = 00000
        self.rating = 0
        self.review_count = 0
        self.category = None


def get_geocode(args):
    """
    Returns GPS coordinates from Google Maps for a given location.
    """
    result = Geocoder.geocode(args.address)
    lat, long = result[0].coordinates
    lat = round(lat, 6)
    long = round(long, 6)
    return (lat, long)


def make_url(args, coords):
    """
    Returns a Yelp API URL based on arguments passed in the command line.
    """
    url = "http://api.yelp.com/v2/search?"
    lat, long = coords
    if args.category:
        url += "&category_filter={0}".format(args.category).replace(" ", "+")
    if args.term:
        url += "&term={0}".format(args.term).replace(" ", "+")
    if args.neighborhood:
        args.neighborhood = args.neighborhood .replace(" ", "+")
        url += "&location={0}".format(args.neighborhood)
    if args.radius:
        url += "&radius_filter={0}".format(int(int(args.radius) * 1609))
    url += "&ll={0},{1}".format(lat, long)
    url += "&sort=2"

    return url


def make_api_call(url, api_creds="yelp.creds"):
    """
    Imports Yelp API credentials from a locally stored file called yelp.creds

    Returns JSON result of API query.
    """
    with open(api_creds, "r") as credentials:
        consumer_key = credentials.readline().strip()[15:]
        consumer_secret = credentials.readline().strip()[18:]
        token = credentials.readline().strip()[8:]
        token_secret = credentials.readline().strip()[15:]

    yelp = OAuth1Session(consumer_key, consumer_secret, token, token_secret)

    api_result = yelp.get(url)
    api_result = api_result.json()
    return api_result


def haversine(origin, destination):
    # Author: Wayne Dyck
    # platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
    lat1, long1 = origin
    lat2, long2 = destination
    radius = 3959  # of earth, in miles

    delta_lat = math.radians(lat2-lat1)
    delta_long = math.radians(long2-long1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) \
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) \
        * math.sin(delta_long/2) * math.sin(delta_long/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = round(radius * c, 2)

    return distance


def generate_coords(origin, density=1, radius=1):
    """
    Returns list of coordinates, given a single origin coordinate (expressed in
    decimal degrees), a radius (expressed in miles), and a density value.
    """
    coords = []
    limit = ((2 * density) + 1)**2  # y = (2x+1)^2
    a, b = origin
    gmap.addradpoint(a, b, (radius*1609), "origin")
    xmax, ymin = ((a + (X_INCREMENT * radius)), ((b - (Y_INCREMENT * radius))))
    xmin, ymax = ((a - (X_INCREMENT * radius)), ((b + (Y_INCREMENT * radius))))
    gmap.addpoint(a, b, "#0000FF")
    a, b = xmin, ymax

    for x in range(0, int(math.sqrt(limit))):
        for y in range(0, int(math.sqrt(limit))):
            lat = float("%.6f" % (a + (x * (X_INCREMENT / density))))
            long = float("%.6f" % (b - (y * (Y_INCREMENT / density))))
            new_coord = (lat, long)
            if new_coord not in coords:
                coords.append(new_coord)

    return coords


def create_search_map(origin, coords, radius_enforced=True, radius=1):
    lat, long = origin
    gmap = pygmaps.maps(lat, long, 14)
    for pair in coords:
        if radius_enforced:
            if haversine(pair, origin) > radius:
                pass
            else:
                lat, long = pair
                gmap.addpoint(lat, long, "#0000FF")
        else:
            lat, long = pair
            gmap.addpoint(lat, long, "#0000FF")
    gmap.draw('./search_map.html')


def parse_results(api_result, items):
    """
    Returns list of Business objects generated by API request.
    """
    for x in range(0, 40):  # 40 is the most results the API will return
        biz = Business()
        try:
            source = api_result["businesses"][x]
            biz.result_position = x+1
            biz.id = source["id"]
            biz.name = source["name"]
            if len(source["location"]["address"]) > 1:
                biz.address = source["location"]["address"][0]
                biz.address += ", " + source["location"]["address"][1]
            else:
                biz.address = source["location"]["display_address"][0]
            biz.city = source["location"]["city"]
            biz.state = source["location"]["state_code"]
            biz.zip = source["location"]["postal_code"]
            biz.rating = str(source["rating"])
            biz.review_count = str(source["review_count"])
            biz.category = source["categories"][0][0]
            item = [biz.result_position, biz.id, biz.name, biz.address,
                    biz.city, biz.state, biz.zip, biz.rating,
                    biz.review_count, biz.category]
            items.append(item)
        except IndexError:
            break
        except KeyError:
            if api_result["error"]:
                print("Error(s) encountered, please see raw_output.txt!")
                write_raw_result(api_result)
                sys.exit(1)
            break
    return items


def scrape_yelp(args, coords):
    items = []
    for coord in coords:
        url = make_url(args, coord)
        result = make_api_call(url)
        items = parse_results(result, items)
    return items


def eliminate_duplicate_results(results):
    old = results
    results = []
    for item in old:
        if item in results:
            pass
        else:
            results.append(item)

    return results


def write_raw_result(api_result):
    """
    Writes raw JSON data to a local file, for debugging purposes.

    If for some reason the script returns an empty CSV file, or complete
    garbage, it could be useful to have this file generated. Such a file would
    reveal any Oauth errors, for example.
    """
    with open("raw_output.txt", "w") as file:
        url = make_url(args, get_geocode(args))
        file.write("API URL Retrieved: {0}\n".format(url))
        json.dump(api_result, file, sort_keys=True, indent=4)


def write_csv_file(items):
    """
    Writes CSV file of returned data from list of Business objects.
    """
    with open("results.csv", "w") as csvout:
        output = csv.writer(csvout)
        output.writerow(["ID", "Name", "Address", "City", "State",
                         "Zip", "Rating", "Review Count", "Category"])
        for row in items:
            output.writerow(row)

origin = get_geocode(args)
results = generate_coords(origin, int(args.density), int(args.radius))
create_search_map(origin, results, True, int(args.radius))
yelp_results = scrape_yelp(args, results)
yelp_results = eliminate_duplicate_results(yelp_results)
write_csv_file(yelp_results)
write_raw_result(yelp_results)
