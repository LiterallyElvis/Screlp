import unittest
import coord_gen

class SortTest(unittest.TestCase):

    def test_distance_calculation(self):
        origin = (30.274294, -97.740504)
        destination = (30.274294, -97.723804)
        self.assertEqual(coord_gen.haversine(origin, destination), 1)
        
if __name__ == '__main__':
    unittest.main()