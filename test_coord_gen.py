import unittest
import coord_gen

class SortTest(unittest.TestCase):

    def test_distance_calculation(self):
        origin = (30.274294, -97.740504)
        destination = (30.274293, -97.723742)
        self.assertEqual(coord_gen.haversine(origin, destination), 1)

    def test_coordinate_generation(self):
        origin = (30.274294, -97.740504)
        proper_coords = [(30.274293, -97.740504), 
                         (30.288769, -97.740504), 
                         (30.274293, -97.723743), 
                         (30.259819, -97.740504), 
                         (30.274293, -97.757265)]

        self.assertEqual(set(proper_coords) & set(coord_gen.generate_coords(origin, 1)))b
        
if __name__ == '__main__':
    unittest.main()