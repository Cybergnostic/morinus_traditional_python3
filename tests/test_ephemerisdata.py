"""Pure ephemeris regression tests: leap year, stations, ingresses, Aries wrap."""
import unittest
import ephemerisdata as e


def fake(start, speed):
    return lambda jd, planet: ((start + speed * jd) % 360.0, speed)


class EphemerisDataTests(unittest.TestCase):
    def test_year_length(self):
        self.assertEqual(e.year_days(2024), 366)
        self.assertEqual(e.year_days(2025), 365)
        self.assertEqual(e.year_days(1900), 365)
        self.assertEqual(e.year_days(2000), 366)

    def test_wrap_and_direction(self):
        self.assertEqual(e.delta(359, 1), 2)
        self.assertEqual(e.delta(1, 359), -2)
        self.assertEqual(e.ingress_crossing(359, 1), (0, 1))
        self.assertEqual(e.ingress_crossing(1, 359), (11, -1))
        self.assertEqual(e.ingress_crossing(29, 31), (1, 1))
        self.assertEqual(e.ingress_crossing(31, 29), (0, -1))
        self.assertIsNone(e.ingress_crossing(10, 11))

    def test_station_vs_exact_speed(self):
        self.assertTrue(e.station_crossing(-0.1, 0.1))
        self.assertTrue(e.station_crossing(-0.1, 0))
        self.assertTrue(e.station_crossing(0.1, 0))
        self.assertFalse(e.station_crossing(0, 0.1))
        self.assertFalse(e.station_crossing(0.1, 0.1))

    def test_refinement_both_directions(self):
        self.assertAlmostEqual(e.bisect(0, 1, lambda t: t - 0.3), 0.3, places=6)
        self.assertAlmostEqual(e.bisect(0, 1, lambda t: 0.7 - t), 0.7, places=6)
        with self.assertRaises(ValueError):
            e.bisect(0, 1, lambda t: t + 2)

    def test_actual_midnight_rows_include_february_29(self):
        result = e.calculate(2024, 2460310.5,
                             lambda jd, planet: (20.0 + planet, 0.01))
        self.assertEqual(len(result.dates), 366)
        self.assertEqual(result.dates[59].isoformat(), '2024-02-29')
        self.assertEqual(len(result.longitudes), 7)
        self.assertEqual(len(result.longitudes[0]), 366)
        self.assertEqual(result.events, [])

    def test_station_and_ingress_event_sampling(self):
        # Every planet goes from direct to retrograde halfway through the year;
        # longitude crosses 30 degrees direct early and backward late.
        def sample(jd, planet):
            t = jd - 2460000.5
            speed = 1.0 - t / 180.0
            lon = (20 + t - t*t / 360.0) % 360
            return lon, speed
        result = e.calculate(2026, 2460000.5, sample)
        stations = [v for v in result.events if v.planet == 0 and v.kind == 'Station']
        self.assertEqual(len(stations), 1)
        self.assertAlmostEqual(stations[0].jd - 2460000.5, 180, places=3)
        ingresses = [v for v in result.events if v.planet == 0 and v.kind == 'Ingress']
        self.assertGreaterEqual(len(ingresses), 1)
        self.assertTrue(ingresses[0].detail.startswith('Ingress '))

    def test_position_format(self):
        self.assertIn('Pis', e.format_position(359.5, 0.5))
        self.assertTrue(e.format_position(12.5, -0.5).endswith(' R'))


if __name__ == '__main__':
    unittest.main()
