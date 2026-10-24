"""Course definition and chronological boundaries for monthly solar returns."""

import unittest

import monthlysolar


class MonthlySolarTests(unittest.TestCase):
    def test_twelve_successive_sign_targets_preserve_natal_degree(self):
        targets = monthlysolar.target_longitudes(359.5)
        self.assertEqual(len(targets), 12)
        self.assertEqual(targets[0], 359.5)
        self.assertEqual(targets[1], 29.5)
        self.assertEqual(targets[11], 329.5)

    def test_twelve_events_start_with_actual_solar_return(self):
        start = 2450000.0
        length = 365.2422
        def crossings(target, estimate):
            return [(estimate + 0.4, (2026, 1, 1, 12, 0, 0))]
        rows = monthlysolar.choose_events(start, start + length, 75.0, crossings)
        self.assertEqual(len(rows), 12)
        self.assertIsNone(rows[0].utc_tuple)
        self.assertAlmostEqual(rows[0].jd, start)
        self.assertEqual(rows[-1].month, 12)
        self.assertTrue(all(a.jd < b.jd for a, b in zip(rows, rows[1:])))

    def test_discard_crossings_outside_solar_year(self):
        with self.assertRaisesRegex(ValueError, 'Missing monthly'):
            monthlysolar.choose_events(1_000_000.0, 1_000_365.25, 75.0,
                                       lambda target, estimate: [(1_000_366.0, (2026, 1, 1, 0, 0, 0))])

    def test_choose_crossing_nearest_expected_month(self):
        def crossings(target, estimate):
            return [
                (estimate + 5.0, (2026, 1, 1, 0, 0, 0)),
                (estimate - 2.0, (2026, 1, 1, 0, 0, 0)),
            ]
        rows = monthlysolar.choose_events(2450000.0, 2450365.24, 45.0, crossings)
        self.assertAlmostEqual(rows[1].jd, 2450000.0 + 365.24 / 12 - 2.0)

    def test_reject_invalid_solar_year_boundaries(self):
        with self.assertRaisesRegex(ValueError, 'successive'):
            monthlysolar.choose_events(2450000.0, 2450400.0, 45.0, lambda *_: [])


if __name__ == '__main__':
    unittest.main()
