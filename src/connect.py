from requests_oauthlib import OAuth1Session
import argparse
import configparser

METERS_PER_MILE = 1609
MAX_YELP_RADIUS = 40000


def make_url(args, coords):
    """
    Returns a Yelp API URL based on arguments passed in the command line.
    """

    url = "http://api.yelp.com/v2/search?"
    lat, long = coords
    if args.term:
        url += "&term={0}".format(args.term).replace(" ", "+")
    if args.radius:
        radius = int((int(args.radius) * METERS_PER_MILE) / int(args.density))
        radius = min(radius, MAX_YELP_RADIUS)
        url += "&radius_filter={0}".format(radius)
    if args.category:
        url += "&category_filter={0}".format(category).replace(" ", "+")
    url += "&ll={0},{1}".format(lat, long)

    return url


def make_api_call(url, api_creds="creds.ini"):
    """
    Imports Yelp API credentials from a locally stored file called yelp.creds

    Returns JSON result of API query.
    """

    config = configparser.ConfigParser()
    config.read('creds.ini')

    consumer_key = config['YELP']['ConsumerKey']
    consumer_secret = config['YELP']['ConsumerSecret']
    token = config['YELP']['Token']
    token_secret = config['YELP']['TokenSecret']

    yelp = OAuth1Session(consumer_key, consumer_secret, token, token_secret)

    api_result = yelp.get(url)
    api_result = api_result.json()
    return api_result
