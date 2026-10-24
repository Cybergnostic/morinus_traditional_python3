"""Regression tests for A3's Lilly-style impediment classification.

Fixtures are intentionally event-driven: this suite tests doctrinal event
ordering separately from the actual Swiss Ephemeris root-finding tests.
"""
import unittest

from aspect_event_search import Event
from horary_impediments import assess


def placements(mars=7, saturn=12, mars_speed=1.0, saturn_speed=.1,
               venus=14, moon=6, moon_speed=13.0):
    return {
        'Saturn': (saturn, saturn_speed),
        'Jupiter': (90, .08),
        'Mars': (mars, mars_speed),
        'Sun': (120, 1.0),
        'Venus': (venus, .0),
        'Mercury': (210, 1.6),
        'Moon': (moon, moon_speed),
    }


def exact(time, a, b, index=0):
    return Event(time, 'aspect', a, b, index)


class HoraryImpedimentsTests(unittest.TestCase):
    def test_direct_application_without_other_events(self):
        review = assess([exact(3, 'Mars', 'Saturn')], 'Mars', 'Saturn',
                        0, placements())
        self.assertEqual(review.initial_motion, 'Applying')
        self.assertEqual(review.target_jd, 3)
        self.assertEqual(review.findings, ())
        self.assertIn('Direct perfection', review.summary)

    def test_not_applying_is_not_a_prohibition(self):
        chart = placements(mars_speed=-1)
        review = assess([exact(3, 'Mars', 'Saturn')], 'Mars', 'Saturn', 0, chart)
        self.assertIsNone(review.target_jd)
        self.assertIn('not applying', review.summary)

    def test_no_contact_in_initial_chart(self):
        review = assess([exact(3, 'Mars', 'Saturn')], 'Mars', 'Saturn',
                        None, placements())
        self.assertIsNone(review.target_jd)
        self.assertEqual(review.findings, ())

    def test_frustration_slow_partner_first_meets_third(self):
        # Mars pursues Saturn; Saturn independently moves toward Venus.
        events = [exact(1, 'Saturn', 'Venus'),
                  exact(4, 'Mars', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertTrue(any(f.kind == 'Frustration'
                            and f.actor == 'Saturn' and f.other == 'Venus'
                            for f in review.findings))

    def test_do_not_call_one_arbitrary_contact_frustration(self):
        # Saturn moving away from Moon, not toward Moon.
        events = [exact(1, 'Saturn', 'Moon'),
                  exact(4, 'Mars', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertFalse(any(f.kind == 'Frustration' for f in review.findings))
        self.assertTrue(any(f.kind == 'Earlier contact' for f in review.findings))

    def test_prohibition_requires_two_contacts_before_original(self):
        events = [exact(1, 'Moon', 'Mars'),
                  exact(2, 'Moon', 'Saturn'),
                  exact(5, 'Mars', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertTrue(any(f.kind == 'Prohibition'
                            and f.actor == 'Moon' for f in review.findings))

    def test_one_contact_does_not_prove_prohibition(self):
        events = [exact(1, 'Moon', 'Saturn'),
                  exact(5, 'Mars', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertFalse(any(f.kind == 'Prohibition' for f in review.findings))

    def test_intermediary_station_downgrades_to_possible(self):
        events = [exact(.5, 'Moon', 'Mars'),
                  Event(1, 'station', 'Moon'),
                  exact(2, 'Moon', 'Saturn'),
                  exact(5, 'Mars', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertTrue(any(f.kind == 'Possible prohibition'
                            for f in review.findings))

    def test_refranation_requires_actual_turn_away(self):
        events = [Event(1, 'station', 'Mars')]
        def where(jd):
            positions = placements()
            positions['Mars'] = (8.0, 1.0 if jd < 1 else -1.0)
            return positions
        review = assess(events, 'Mars', 'Saturn', 0, placements(), where)
        self.assertTrue(any(f.kind == 'Refranation' for f in review.findings))

    def test_station_without_positions_is_not_confirmed_refranation(self):
        events = [Event(1, 'station', 'Mars')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertTrue(any(f.kind == 'Possible refranation'
                            for f in review.findings))
        self.assertFalse(any(f.kind == 'Refranation'
                             for f in review.findings))

    def test_station_of_non_applying_partner_is_not_refranation(self):
        events = [Event(1, 'station', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertTrue(any(f.kind == 'Station' for f in review.findings))
        self.assertFalse(any('refranation' in f.kind.lower()
                             for f in review.findings))

    def test_change_of_sign_visible_not_automatic_denial(self):
        events = [Event(1, 'ingress', 'Mars'),
                  exact(2, 'Mars', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertEqual(review.target_jd, 2)
        self.assertTrue(any(f.kind == 'Sign change' for f in review.findings))
        self.assertFalse(any(f.kind == 'Prohibition' for f in review.findings))

    def test_only_same_aspect_matches_original_application(self):
        events = [exact(2, 'Mars', 'Saturn', 1)]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertIsNone(review.target_jd)
        self.assertIn('No direct perfection', review.summary)

    def test_event_after_perfection_cannot_prohibit(self):
        events = [exact(1, 'Mars', 'Saturn'),
                  exact(2, 'Moon', 'Mars'),
                  exact(3, 'Moon', 'Saturn')]
        review = assess(events, 'Mars', 'Saturn', 0, placements())
        self.assertEqual(review.findings, ())

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            assess([], 'Mars', 'Mars', 0, placements())
        with self.assertRaises(ValueError):
            assess([], 'Mars', 'Saturn', 5, placements())


if __name__ == '__main__':
    unittest.main()
