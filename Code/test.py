import unittest
from io import StringIO
from customer import Customer
from reservation import Reservation
import main

class Test(unittest.TestCase):

    def test_read_fully_fail(self):
        test_data = "KaiusKarvo"
        self.input_file = StringIO(test_data)
        with self.assertRaises(OSError):
            maintest = main.read_fully(15, self.input_file)

    def test_read_fully_success(self):
        test_data = "KaiusKarvo"
        self.input_file = StringIO(test_data)
        self.assertEqual(main.read_fully(10, self.input_file), "KaiusKarvo")

    def test_get_chunk_name_and_size(self):
        test_data = "NUM15"
        self.input_file = StringIO(test_data)
        self.assertEqual(main.get_chunk_name(self.input_file), "NUM")
        self.assertEqual(main.get_chunk_size(self.input_file), 15)

    def test_chunk_handling_success(self):
        test_data = "NAM10KaiusKarvo"
        self.input_file = StringIO(test_data)
        self.assertEqual(main.get_chunk_name(self.input_file), "NAM")
        self.assertEqual(main.get_chunk_size(self.input_file), 10)
        self.assertEqual(main.read_fully(10, self.input_file), "KaiusKarvo")

    def test_chunk_handling_failure(self):
        test_data = "NAM10Kaius"
        self.input_file = StringIO(test_data)
        self.assertEqual(main.get_chunk_name(self.input_file), "NAM")
        self.assertEqual(main.get_chunk_size(self.input_file), 10)
        with self.assertRaises(OSError):
            readtest = main.read_fully(10, self.input_file)


    def close_silently(self, r):
        try:
            r.close()
        except OSError:
            """ignore"""

if __name__ == "__main__":
    unittest.main()
