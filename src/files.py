import json
import csv
import connect
import geog


def write_raw_result(api_result, args):
    """
    Writes raw JSON data to a local file, for debugging purposes.

    If for some reason the script returns an empty CSV file, or complete
    garbage, it could be useful to have this file generated. Such a file would
    reveal any Oauth errors, for example.
    """
    with open("raw_output.txt", "w") as file:
        url = connect.make_url(args, geog.get_geocode(args))
        file.write("API URL Retrieved: {0}\n".format(url))
        json.dump(api_result, file, sort_keys=True, indent=4)


def write_csv_file(items):
    """
    Writes CSV file of returned data from list of Business objects.
    """
    with open("results.csv", "w") as csvout:
        output = csv.writer(csvout)
        output.writerow(["Rank", "ID", "Name", "Address", "City", "State",
                         "Zip", "Rating", "Review Count", "Category", "URL"])
        output.writerows(items)
