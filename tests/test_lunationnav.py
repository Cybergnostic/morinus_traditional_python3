"""Unit tests for signed lunar-phase crossings (no ephemeris required)."""
import unittest
import lunationnav as n


def synthetic(jd):
    """Linear relative motion: 360 degrees every 30 days."""
    return 0.0, (jd * 12.0) % 360.0


class LunationNavigatorTests(unittest.TestCase):
    def test_phase_wrap(self):
        self.assertEqual(n.phase_difference(359, 0, 0), -1)
        self.assertEqual(n.phase_difference(1, 0, 0), 1)
        self.assertEqual(n.phase_difference(181, 0, 180), 1)

    def test_reject_opposite_discontinuity(self):
        self.assertTrue(n.crossing(-5, 5))
        self.assertFalse(n.crossing(-179, 179))
        self.assertFalse(n.crossing(5, -5))

    def test_bisection(self):
        jd = n.refine(-1.0, 1.0, 0, synthetic)
        self.assertLess(abs(jd), 1e-6)

    def test_sorted_alternating_new_and_full(self):
        events = n.find_events(30.0, synthetic, half_window=36)
        self.assertGreaterEqual(len(events), 4)
        self.assertEqual(events, sorted(events))
        self.assertLess(abs(events[0][0] - -0.0), 15.1)
        for first, second in zip(events, events[1:]):
            self.assertNotEqual(first[1], second[1])
            self.assertAlmostEqual(second[0] - first[0], 15.0, places=3)

    def test_natal_input_is_not_modified(self):
        jd = 12345.0
        n.find_events(jd, synthetic, half_window=20)
        self.assertEqual(jd, 12345.0)


if __name__ == '__main__':
    unittest.main()
