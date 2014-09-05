import math

X_INCREMENT = .014474
Y_INCREMENT = .016761


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


def generate_coords(origin, radius=1, density=0):
    coords = []
    limit = int(1+((2**density)**2))
    a, b = origin
    xmax, ymin = ((a + (X_INCREMENT * radius)), ((b - (Y_INCREMENT * radius))))
    xmin, ymax = ((a - (X_INCREMENT * radius)), ((b + (Y_INCREMENT * radius))))
    x, y = xmin, ymax

    for x in range(0, limit):
        for y in range(0, limit):
            new_coord = ((a + (x * X_INCREMENT)), (b - (y * Y_INCREMENT)))
            if new_coord not in coords:
                coords.append(new_coord)

    return coords

def enforce_radius(coords, radius):
    for pair in coords:
        lat, long = pair
        if haversine(lat, long) > radius:
            coords.remove(pair)

    return coords