import math
import pygmaps

X_INCREMENT = .014474
Y_INCREMENT = .016761

gmap = pygmaps.maps(30.233974, -97.732430, 13)


def haversine(origin, destination):
    # Author: Wayne Dyck
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
                if haversine(origin, new_coord) <= radius:
                    gmap.addpoint(lat, long, "#0000FF")
                    coords.append(new_coord)

    return coords


def enforce_radius(coords, radius):
    for pair in coords:
        lat, long = pair
        if haversine(lat, long) >= radius:
            coords.remove(pair)

    return coords

print(generate_coords((30.233974, -97.732430), 3))
gmap.draw('./gmap.html')
