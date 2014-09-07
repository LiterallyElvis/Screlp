# -*- coding: utf-8 -*-
import math
import pygmaps

X_INCREMENT = .014474
Y_INCREMENT = .016761

origin = (30.274294, -97.740504)
gmap = pygmaps.maps(30.274294, -97.740504, 14)

# begin function borrowed from the internet


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

# end function borrowed from the internet


def generate_coords(origin, density=1, radius=1):
    """
    Returns list of coordinates, given a single origin coordinate (expressed in
    decimal degrees), a radius (expressed in miles), and a density value.
    """
    coords = []
    limit = ((2 * density) + 1)**2  # y = (2x+1)²
    a, b = origin
    gmap.addradpoint(a, b, (radius*1609.34), "origin")
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


def create_map(coords, radius_enforced=True, radius=1):
    for pair in coords:
        if radius_enforced:
            if haversine(pair, origin) > radius:
                pass
            else:
                lat, long = pair
                gmap.addpoint(lat, long, "#0000FF")
    gmap.draw('./gmap.html')

create_map(generate_coords(origin, 3))
