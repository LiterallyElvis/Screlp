from requests_oauthlib import OAuth1Session
import json
import csv


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

    def __repr__(self):
        return ("\nID: " + self.id + "\n" +
                "Name: " + self.name + "\n" +
                "Address: " + self.address + "\n" +
                "City: " + self.city + "\n" +
                "State: " + self.state + "\n" +
                "Zip Code: " + self.zip + "\n" +
                "Rating: " + self.rating + "\n" +
                "Category: " + self.category + "\n")

url = 'http://api.yelp.com/v2/search?category_filter=icecream&location=Austin'


def make_api_call(api_creds="creds.config", url):
    with open(filename, 'r') as creds:
        consumer_key = creds.readline().strip()
        consapi_resultumer_secret = creds.readline().strip()
        token = creds.readline().strip()
        token_secret = creds.readline().strip()

    yelp = OAuth1Session(consumer_key, consumer_secret, token, token_secret)

    api_result = yelp.get(url)
    api_result = api_result.json()
    return api_result


def write_raw_result(api_result):
    with open('raw_Yelp_JSON_data.txt', 'w') as file:
        json.dump(api_result, file, sort_keys=True, indent=4)


def fetch_results(api_result):
    for x in range(0, 40):
        items = []
        biz = Business()
        try:
            source = api_result['businesses'][x]
            biz.id = source['id']
            biz.name = source['name']
            if len(source['location']['address']) > 1:
                biz.address = source['location']['address'][0]
                biz.address += "\n" + source['location']['address'][1]
            else:
                biz.address = source['location']['display_address'][0]
            biz.city = source['location']['city']
            biz.state = source['location']['state_code']
            biz.zip = source['location']['postal_code']
            biz.rating = str(source['rating'])
            biz.review_count = str(source['review_count'])
            biz.category = source['categories'][0][0]
            item = [biz.id, biz.name, biz.address, biz.city, biz.state,
                    biz.zip, biz.rating, biz.review_count, biz.category]
            items.append(item)
        except IndexError:
            break
    return items


def write_csv_file(items):
    with open('results.csv', 'w') as csvout:
        output = csv.writer(csvout)
        output.writerow(['ID', 'Name', 'Address', 'City', 'State',
                         'Zip', 'Rating', 'Review Count', 'Category'])
        for row in items:
            output.writerow(row)
