"""Morinus's bundled Swiss Ephemeris C-extension return contract."""
import unittest
from swestatus import status_code


class SwissStatusTests(unittest.TestCase):
    def test_wrapped_success(self):
        self.assertEqual(status_code((258,)), 258)
        self.assertEqual(status_code([2]), 2)

    def test_wrapped_failure(self):
        self.assertLess(status_code((-1,)), 0)

    def test_plain_status_for_test_doubles(self):
        self.assertEqual(status_code(2), 2)
        self.assertLess(status_code(-1), 0)

    def test_reject_unexpected_status_shape(self):
        with self.assertRaises(ValueError):
            status_code(())
        with self.assertRaises(ValueError):
            status_code((2, 3))
        with self.assertRaises(TypeError):
            status_code(('2',))


if __name__ == '__main__':
    unittest.main()
