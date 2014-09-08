# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session


def make_url(args, coords):
    """
    Returns a Yelp API URL based on arguments passed in the command line.
    """
    url = "http://api.yelp.com/v2/search?"
    lat, long = coords
    if args.term:
        url += "&term={0}".format(args.term).replace(" ", "+")
    if args.radius:
        radius = int((int(args.radius) * 1609) / int(args.density))
        url += "&radius_filter={0}".format(radius)
    url += "&ll={0},{1}".format(lat, long)

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
