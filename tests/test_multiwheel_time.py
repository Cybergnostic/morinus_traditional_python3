import unittest

from multiwheel_time import UNITS, shift


class TransitTimeTests(unittest.TestCase):
    def test_all_six_units(self):
        source = (2026, 10, 23, 12, 34, 56)
        expected = ((2027, 10, 23, 12, 34, 56),
                    (2026, 11, 23, 12, 34, 56),
                    (2026, 10, 24, 12, 34, 56),
                    (2026, 10, 23, 13, 34, 56),
                    (2026, 10, 23, 12, 35, 56),
                    (2026, 10, 23, 12, 34, 57))
        for unit, result in zip(UNITS, expected):
            self.assertEqual(shift(source, unit, True), result)
            self.assertEqual(shift(result, unit, False), source)

    def test_month_clamps_day(self):
        self.assertEqual(shift((2026, 1, 31, 10, 0, 0), 'Month', True),
                         (2026, 2, 28, 10, 0, 0))
        self.assertEqual(shift((2028, 1, 31, 10, 0, 0), 'Month', True),
                         (2028, 2, 29, 10, 0, 0))

    def test_year_clamps_leap_day(self):
        self.assertEqual(shift((2028, 2, 29, 0, 0, 0), 'Year', True),
                         (2029, 2, 28, 0, 0, 0))

    def test_boundary_wraps(self):
        self.assertEqual(shift((2026, 12, 31, 23, 59, 59), 'Sec', True),
                         (2027, 1, 1, 0, 0, 0))
        self.assertEqual(shift((2027, 1, 1, 0, 0, 0), 'Sec', False),
                         (2026, 12, 31, 23, 59, 59))

    def test_outside_supported_years(self):
        self.assertIsNone(shift((1, 1, 1, 0, 0, 0), 'Year', False))
        self.assertIsNone(shift((9999, 12, 1, 0, 0, 0), 'Month', True))
        with self.assertRaises(ValueError):
            shift((2026, 1, 1, 0, 0, 0), 'Fortnight', True)


if __name__ == '__main__':
    unittest.main()
