import math 

# MILE_IN_COORDS = 0.0145
MILE_IN_COORDS = 14500
KM_IN_COORDS = 0.009

# Author: Wayne Dyck
def haversine(origin, destination):
    lat1, long1 = origin
    lat2, long2 = destination
    radius = 3959 # of earth, in miles
 
    delta_lat = math.radians(lat2-lat1)
    delta_long = math.radians(long2-long1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(delta_long/2) * math.sin(delta_long/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = round(radius * c, 1    )
 
    return dist