import math 

# MILE_IN_COORDS = 0.0145
MILE_IN_COORDS = 14500
KM_IN_COORDS = 0.009

origin = (30.272738, -97.741064)

radius = 5 * MILE_IN_COORDS
coords = []

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step


def generate_coords(origin, radius, density=radius):
    a, b = origin
    int_a, int_b = int(a), int(b)
    a = int((a % 1)*1000000)
    print("A: ", a)
    b = int((b % 1)*1000000)
    print("B: ", b)
    for x in range(a, (a + radius), 14500):
        for y in range(b, (b + radius), 14500):
            new_x = int_a + ((a + 14500) / 1000000)
            new_y = int_b + ((b + 14500) / 1000000)
            new_coords = (new_x, new_y)
            neg_coords = (new_x * -1, new_y * -1)
            if new_coords not in coords:
                coords.append(new_coords)
            if neg_coords not in coords:
                coords.append(neg_coords)
                
    return coords

print(generate_coords(origin, radius))