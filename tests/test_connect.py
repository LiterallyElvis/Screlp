import unittest
import connect as con


class SortTest(unittest.TestCase):

    def test_make_url_input_validation(self):
        bad_args = "whatever"
        bad_coords = 3j
        self.assertRaises(TypeError, con.make_url, bad_args, bad_coords)

    def test_make_api_call_input_validation(self):
        bad_url = 3.14
        self.assertRaises(TypeError, con.make_api_call, bad_url)


if __name__ == '__main__':
    unittest.main()
