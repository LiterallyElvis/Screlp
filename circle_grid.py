import math 

MILE_IN_COORDS = 0.0145
KM_IN_COORDS = 0.009

origin = 30.272738, -97.741064

radius = 5
coords = []
complete = False

for x in range(0, radius + 1):
    for y in range(0, radius + 1):
        new_coords = (x, y)
        other_coords = (x * -1, y * -1)

        limit = math.hypot(x, y)
        neg_limit = math.hypot(x * -1, y * -1)
                
        if limit > radius or neg_limit > radius:
            pass
        else:
            if new_coords not in coords:
                coords.append(new_coords)
        
            if other_coords not in coords:
                coords.append(other_coords)
        
print(coords)