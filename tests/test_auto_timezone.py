import unittest
from unittest.mock import patch

from auto_timezone import TimezoneLookupError, resolve_timezone


class FakeFinder:
    def __init__(self, **kwargs):
        pass

    def timezone_at(self, **kwargs):
        return "Europe/Belgrade"


class AutoTimezoneTests(unittest.TestCase):
    def test_winter_and_summer(self):
        with patch("timezonefinder.TimezoneFinder", FakeFinder):
            self.assertEqual(resolve_timezone(1988, 1, 15, 12, 0, 0, 43.32, 21.9)[1:3], (60, False))
            self.assertEqual(resolve_timezone(1988, 6, 8, 19, 15, 0, 43.32, 21.9)[1:3], (60, True))

    def test_nonexistent_time_rejected(self):
        with patch("timezonefinder.TimezoneFinder", FakeFinder):
            with self.assertRaises(TimezoneLookupError):
                resolve_timezone(2026, 3, 29, 2, 30, 0, 43.32, 21.9)

    def test_ambiguous_time_rejected(self):
        with patch("timezonefinder.TimezoneFinder", FakeFinder):
            with self.assertRaises(TimezoneLookupError):
                resolve_timezone(2026, 10, 25, 2, 30, 0, 43.32, 21.9)

    def test_old_dates_warn(self):
        with patch("timezonefinder.TimezoneFinder", FakeFinder):
            self.assertTrue(resolve_timezone(1945, 1, 1, 12, 0, 0, 43.32, 21.9)[3])


if __name__ == "__main__":
    unittest.main()
