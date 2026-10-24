"""Pure rules for course-based planetary divisions."""

import unittest
from datetime import datetime, timedelta, timezone

import divisions


UTC = timezone.utc
START = datetime(2026, 6, 8, 17, 42, tzinfo=UTC)
END = START + timedelta(days=365, hours=6)
SOLAR_LONGITUDES = {
    'Mars': 355.0,
    'Moon': 5.0,
    'Venus': 45.0,
    'Mercury': 100.0,
    'Saturn': 150.0,
    'Jupiter': 200.0,
    'Sun': 300.0,
}


class DivisionsTest(unittest.TestCase):
    def test_valens_durations_are_exactly_365_days(self):
        self.assertEqual(sum(divisions.VALENS_DAYS.values()), 365)

    def test_first_ruler_is_annual_profection_lord(self):
        # Aries rising, twenty-four complete years later: Aries/Mars again.
        result = divisions.calculate_divisions(
            START, END, 5.0, 2002, 2026, 18.0, SOLAR_LONGITUDES,
        )
        self.assertEqual(result.profected_sign, 0)
        self.assertEqual(result.year_ruler, 'Mars')
        self.assertEqual(
            tuple(period.ruler for period in result.periods),
            ('Mars', 'Moon', 'Venus', 'Mercury', 'Saturn', 'Jupiter', 'Sun'),
        )

    def test_periods_are_contiguous_and_cover_solar_year(self):
        result = divisions.calculate_divisions(
            START, END, 5.0, 2002, 2026, 18.0, SOLAR_LONGITUDES,
        )
        self.assertEqual(result.periods[0].start, START)
        self.assertEqual(result.periods[-1].end, END)
        self.assertEqual(result.periods[0].nominal_days, 42)
        self.assertEqual(result.periods[-1].nominal_days, 53)
        for current, following in zip(result.periods, result.periods[1:]):
            self.assertEqual(current.end, following.start)
        self.assertEqual(result.periods[0].solar_house, 12)

    def test_annual_sign_moves_one_sign_per_year(self):
        self.assertEqual(divisions.annual_sign(359.9, 2000, 2000), 11)
        self.assertEqual(divisions.annual_sign(359.9, 2000, 2001), 0)
        self.assertEqual(divisions.annual_sign(359.9, 2000, 2012), 11)

    def test_missing_planet_is_rejected(self):
        with self.assertRaises(ValueError):
            divisions.secondary_order('Mars', {'Mars': 20.0})

    def test_naive_dates_are_rejected(self):
        with self.assertRaises(ValueError):
            divisions.calculate_divisions(
                START.replace(tzinfo=None), END, 5.0, 2002, 2026, 18.0,
                SOLAR_LONGITUDES,
            )


if __name__ == '__main__':
    unittest.main()
