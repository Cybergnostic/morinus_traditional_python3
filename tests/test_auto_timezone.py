import importlib.util
import sys
import types
import unittest
from unittest.mock import patch

from auto_timezone import TimezoneLookupError, resolve_timezone


class FakeFinder:
    zone = "Europe/Belgrade"

    def __init__(self, **kwargs):
        pass

    def timezone_at(self, **kwargs):
        return self.zone


class DublinFinder(FakeFinder):
    zone = "Europe/Dublin"


class SeaFinder(FakeFinder):
    zone = "Etc/GMT+2"


def finder(cls):
    """Stand in for the timezonefinder package (installed or not)."""
    return patch.dict(sys.modules, {"timezonefinder": types.SimpleNamespace(TimezoneFinder=cls)})


class AutoTimezoneTests(unittest.TestCase):
    def test_winter_and_summer(self):
        with finder(FakeFinder):
            self.assertEqual(resolve_timezone(1988, 1, 15, 12, 0, 0, 43.32, 21.9)[1:3], (60, False))
            self.assertEqual(resolve_timezone(1988, 6, 8, 19, 15, 0, 43.32, 21.9)[1:3], (60, True))

    def test_nonexistent_time_rejected(self):
        with finder(FakeFinder):
            with self.assertRaises(TimezoneLookupError):
                resolve_timezone(2026, 3, 29, 2, 30, 0, 43.32, 21.9)

    def test_ambiguous_time_rejected(self):
        with finder(FakeFinder):
            with self.assertRaises(TimezoneLookupError):
                resolve_timezone(2026, 10, 25, 2, 30, 0, 43.32, 21.9)

    def test_old_dates_warn(self):
        with finder(FakeFinder):
            self.assertTrue(resolve_timezone(1945, 1, 1, 12, 0, 0, 43.32, 21.9)[3])

    def test_irish_negative_dst(self):
        # IANA counts Irish winter time as -1h DST; Morinus gets the total offset
        with finder(DublinFinder):
            self.assertEqual(resolve_timezone(2020, 1, 15, 12, 0, 0, 53.35, -6.26)[1:3], (0, False))
            self.assertEqual(resolve_timezone(2020, 7, 15, 12, 0, 0, 53.35, -6.26)[1:3], (60, False))

    def test_sea_warns(self):
        with finder(SeaFinder):
            name, minutes, dst, warning = resolve_timezone(2000, 1, 1, 12, 0, 0, 0.0, -30.0)
            self.assertEqual((minutes, dst), (-120, False))
            self.assertIn("at sea", warning)


@unittest.skipUnless(importlib.util.find_spec("timezonefinder"), "timezonefinder not installed")
class RealLookupTests(unittest.TestCase):
    def test_places(self):
        self.assertEqual(resolve_timezone(1988, 6, 8, 19, 15, 0, 43.32, 21.9)[:3], ("Europe/Belgrade", 60, True))
        self.assertEqual(resolve_timezone(2000, 7, 1, 12, 0, 0, 40.7, -74.0)[:3], ("America/New_York", -300, True))
        self.assertEqual(resolve_timezone(2000, 1, 1, 12, 0, 0, 22.57, 88.36)[:3], ("Asia/Kolkata", 330, False))


if __name__ == "__main__":
    unittest.main()
