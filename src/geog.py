from pygeocoder import Geocoder
import math
import pygmaps
from time import strftime, localtime

X_INCREMENT = .014474  # approximately one latitude mile in decimal degrees
Y_INCREMENT = .016761  # approximately one longitude mile in decimal degrees
METERS_PER_MILE = 1609
EARTH_RADIUS_IN_MILES = 3959  # radius of earth, in miles
gmap = pygmaps.maps(0.0, 0.0, 14)


def get_geocode(args):
    """
    Returns GPS coordinates from Google Maps for a given location.
    """
    result = Geocoder.geocode(args.address)
    lat, long = result[0].coordinates
    lat = round(lat, 6)
    long = round(long, 6)
    return (lat, long)


def haversine(origin, destination):
    # Author: Wayne Dyck
    # platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
    lat1, long1 = origin
    lat2, long2 = destination
    EARTH_RADIUS_IN_MILES = 3959

    delta_lat = math.radians(lat2-lat1)
    delta_long = math.radians(long2-long1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) \
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) \
        * math.sin(delta_long/2) * math.sin(delta_long/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = round(EARTH_RADIUS_IN_MILES * c, 2)

    return distance


def generate_coords(origin, density=1, radius=1):
    """
    Returns list of coordinates, given a single origin coordinate (expressed in
    decimal degrees), a radius (expressed in miles), and a density value.
    """
    coords = []
    limit = ((2 * density) + 1)**2  # y = (2x+1)²
    a, b = origin
    gmap.addradpoint(a, b, (radius * METERS_PER_MILE), "origin")
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
    gmap = pygmaps.maps(lat, long, 14)  # 14 is the map's zoom level
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
    gmap.draw("./search_map_" + strftime("%H-%M-%S", localtime()) + ".html")
