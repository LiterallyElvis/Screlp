from requests_oauthlib import OAuth1Session
from pygeocoder import Geocoder
import json
import csv
import argparse

parser = argparse.ArgumentParser(description="Fetches Yelp results.")
parser.add_argument("-c", "--category", action="store", dest="category_filter",
                    help="Category on yelp to search for")
parser.add_argument("-n", "--neighborhood", action="store",
                    dest="neighborhood", help="Category on yelp to search for")
parser.add_argument("-t", "--term", action="store", dest="term",
                    help="Category on yelp to search for")
parser.add_argument("-a", "--address", action="store", dest="address",
                    required=True, help="Address to base query upon")
parser.add_argument("-r", "--radius", action="store", dest="radius", default=1,
                    help="Radius in miles from origin coordinate.")
parser.add_argument("-d", "--density", action="store", dest="density",
                    default=0, help="Grid density")
parser.add_argument("-file", action="store", dest="filename",
                    default="results.csv", help="Filename to save results as.")

args = parser.parse_args()


class Business:
    def __init__(self):
        self.id = None
        self.name = None
        self.address = None
        self.city = None
        self.state = None
        self.zip = 00000
        self.rating = 0
        self.review_count = 0
        self.category = None


def make_url(args, coords):
    url = "http://api.yelp.com/v2/search?"
    lat, long = coords
    if args.category_filter:
        url += "&category_filter={0}".format(args.category_filter)
    if args.term:
        url += "&term={0}".format(args.term)
    if args.neighborhood:
        url += "&location={0}".format(args.neighborhood)
    location = "cll={0},{1}".format(lat, long)
    return url


def get_coords(args):
    result = Geocoder.geocode(args.address)
    return result[0].coordinates


def make_api_call(url, api_creds="creds.config"):
    with open(api_creds, "r") as creds:
        consumer_key = creds.readline().strip()
        consumer_secret = creds.readline().strip()
        token = creds.readline().strip()
        token_secret = creds.readline().strip()

    yelp = OAuth1Session(consumer_key, consumer_secret, token, token_secret)

    api_result = yelp.get(url)
    api_result = api_result.json()
    return api_result


def write_raw_result(api_result):
    with open("raw_Yelp_JSON_data.txt", "w") as file:
        json.dump(api_result, file, sort_keys=True, indent=4)


def fetch_results(api_result):
    items = []
    for x in range(0, 40):
        biz = Business()
        try:
            source = api_result["businesses"][x]
            biz.id = source["id"]
            biz.name = source["name"]
            if len(source["location"]["address"]) > 1:
                biz.address = source["location"]["address"][0]
                biz.address += "\n" + source["location"]["address"][1]
            else:
                biz.address = source["location"]["display_address"][0]
            biz.city = source["location"]["city"]
            biz.state = source["location"]["state_code"]
            biz.zip = source["location"]["postal_code"]
            biz.rating = str(source["rating"])
            biz.review_count = str(source["review_count"])
            biz.category = source["categories"][0][0]
            item = [biz.id, biz.name, biz.address, biz.city, biz.state,
                    biz.zip, biz.rating, biz.review_count, biz.category]
            items.append(item)
        except IndexError:
            break
    return items


def write_csv_file(items):
    with open("results.csv", "w") as csvout:
        output = csv.writer(csvout)
        output.writerow(["ID", "Name", "Address", "City", "State",
                         "Zip", "Rating", "Review Count", "Category"])
        for row in items:
            output.writerow(row)

write_csv_file(fetch_results(make_api_call(make_url(args))))
