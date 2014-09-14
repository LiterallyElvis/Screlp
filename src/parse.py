import sys
import connect
import files
from collections import namedtuple

items = []


def parse_results(api_result, items, url, args):
    """
    Takes JSON result from Yelp query and uses each individual result to
    populate a Business object. Appends business object to list of business
    objects for later manipulation.
    """
    for x in range(0, api_result["total"]):
        Business = namedtuple("business", ["result_position", "id", "name",
                                           "address", "city", "state", "zip",
                                           "rating", "review_count",
                                           "category", "query_performed"])
        item = []
        try:
            source = api_result["businesses"][x]
            item.append(x+1)
            item.append(source["id"])
            item.append(source["name"])
            if len(source["location"]["address"]) > 1:
                item.append(source["location"]["address"][0] + ", " +
                            source["location"]["address"][1])
            else:
                item.append(source["location"]["display_address"][0])
            item.append(source["location"]["city"])
            item.append(source["location"]["state_code"])
            item.append(source["location"]["postal_code"])
            item.append(str(source["rating"]))
            item.append(str(source["review_count"]))
            item.append(source["categories"][0][0])
            url = url.replace("http://api.yelp.com/v2/search?", "")
            item.append(url)
            biz = Business._make(item)
            items.append(biz)
        except IndexError:
            break
        except KeyError:
            try:
                if api_result["error"]:
                    print("Error(s) encountered, please see raw_output.txt!")
                    files.write_raw_result(api_result, args)
                    sys.exit(1)
            except:
                files.write_raw_result(api_result, args)
    items = list(set(items))
    return items


def scrape_yelp(args, coords):
    """
    Uses list of generated coordinates to:

        1) Generate an API query URL
        2) Visit that URL and retrieve results
        3) Parse the JSON received

    Then returns the parsed results as a list.
    """
    items = []
    for coord in coords:
        url = connect.make_url(args, coord)
        result = connect.make_api_call(url)
        items = parse_results(result, items, url, args)
    return items
