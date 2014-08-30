from requests_oauthlib import OAuth1Session

consumer_key = ''
consumer_secret = ''
token = ''
token_secret = ''

yelp = OAuth1Session(consumer_key, consumer_secret, token, token_secret)

url = 'http://api.yelp.com/v2/search?category_filter=icecream&location=Austin'
response = yelp.get(url)
response = response.json()

class Business:
    def __init__(self, name, street, city, zip, rating, category):
        self.name = None
        self.street = None
        self.city = None
        self.zip = 00000
        self.rating = 0
        self.category = None

    def __repr__(self):
        return ("\nName: " + self.name + "\n" +
                "Address: " + self.street + "\n" +
                "City: " + self.city + "\n" +
                "Zip Code: " + self.zip + "\n" + 
                "Rating: " + self.rating + "\n" + 
                "Category: " + self.category + "\n")

results = []

for x in range(0, 40):
	business = Business("", "", "", "", "", "")
	try:
		business.name = response['businesses'][x]['name']
		business.street = response['businesses'][x]['location']['display_address'][0]
		business.city = response['businesses'][x]['location']['city']
		business.city += ", " + response['businesses'][x]['location']['state_code']
		business.zip = response['businesses'][x]['location']['postal_code']
		business.rating = str(response['businesses'][x]['rating'])
		business.category = response['businesses'][x]['categories'][0][0]
		results.append(business)
	except IndexError:
		break

print(results)
