"""Calculation-level regression tests for the optional traditional aspect engine."""
import unittest
import traditional_aspects as t


class TraditionalAspectTests(unittest.TestCase):
    def test_course_orbs(self):
        self.assertEqual(t.COURSE_ORBS, (9, 9, 8, 15, 7, 7, 12))

    def test_larger_orb_only(self):
        # Course doctrine: the larger orb; never summed, never half-orbs.
        self.assertEqual(t.combine_orbs(15, 7), 15)
        self.assertEqual(t.combine_orbs(7, 12), 12)

    def test_venus_moon_ten_degrees_apart_are_configured(self):
        venus, moon = 7.0, 12.0
        r = t.evaluate(0, 10, 1.2, 13, venus, moon)  # Venus 0 Ari, Moon 10 Ari
        self.assertIsNotNone(r)
        self.assertEqual(r.index, 0)
        self.assertIsNone(t.evaluate(0, 13, 1.2, 13, venus, moon))

    def test_sun_moon_contact_is_fifteen_not_twenty_seven(self):
        # Sun 22, Moon 7 of the same sign: 15 within the Sun's orb.
        self.assertIsNotNone(t.evaluate(22, 7, 1, 13, 15, 12))
        # Sun 28, Moon 12 of the same sign: 16 apart, no contact.
        self.assertIsNone(t.evaluate(28, 12, 1, 13, 15, 12))

    def test_all_five_major_aspects(self):
        for i, angle in enumerate(t.ASPECT_ANGLES):
            with self.subTest(angle=angle):
                r = t.evaluate(10, 10 + angle, 1, 0, 9, 9)
                self.assertIsNotNone(r)
                self.assertEqual(r.index, i)
                self.assertTrue(r.exact)

    def test_sign_configuration_distinct_from_degree_orb(self):
        self.assertEqual(t.sign_configuration(0, 85), 1)  # Aries to Gemini
        self.assertIsNone(t.evaluate(0, 85, 0, 0, 9, 9))

    def test_out_of_sign_conjunction_wrap(self):
        r = t.evaluate(359, 1, 0, 0, 9, 9)
        self.assertEqual(r.index, 0)
        self.assertTrue(r.out_of_sign)
        self.assertEqual(r.deviation, 2)

    def test_out_of_sign_limit(self):
        self.assertIsNotNone(t.evaluate(358, 1, 0, 0, 9, 9))
        self.assertIsNone(t.evaluate(357, 1, 0, 0, 9, 9))
        # The course example: Mercury 27 Gemini and Jupiter 1 Cancer are
        # 4 degrees apart, no conjunction; Mercury on 28 Gemini, conjunction.
        self.assertIsNone(t.evaluate(87, 91, 1, 0.1, 7, 9))
        self.assertIsNotNone(t.evaluate(88, 91, 1, 0.1, 7, 9))

    def test_no_separation_across_a_sign_change(self):
        # Sun 28 Taurus, Moon 7 Aquarius: they see each other by square,
        # but are not configured (the Moon is outside the Sun's orb).
        self.assertIsNone(t.evaluate(58, 307, 1, 13, 15, 12))
        # Moon 13 Aquarius: the square begins, applying.
        r = t.evaluate(58, 313, 1, 13, 15, 12)
        self.assertEqual(r.index, 2)
        self.assertTrue(r.applying)
        # Mars 14 Leo, Sun 28 Taurus: still within the Sun's orb, separating.
        r = t.evaluate(58, 134, 1, 0.5, 15, 8)
        self.assertEqual(r.index, 2)
        self.assertTrue(r.separating)

    def test_application_and_separation_direct(self):
        approaching = t.evaluate(0, 63, 2, 0, 9, 9)
        departing = t.evaluate(0, 63, 0, 2, 9, 9)
        self.assertTrue(approaching.applying)
        self.assertTrue(departing.separating)

    def test_retrograde_motion_and_zero_crossing(self):
        self.assertTrue(t.evaluate(359, 2, 0, -1, 9, 9).applying)
        self.assertTrue(t.evaluate(359, 2, 0, 1, 9, 9).separating)

    def test_double_application_direct_and_retrograde(self):
        r = t.evaluate(0, 63, 2, -1, 9, 9)
        self.assertIsNotNone(r)
        self.assertTrue(r.double_applying)
        self.assertFalse(r.double_separating)
        self.assertTrue(r.applying)
        self.assertEqual(t.motion_status(63, 0, -1, 2, 60), "Double application")

    def test_double_separation_direct_and_retrograde(self):
        r = t.evaluate(0, 63, -2, 1, 9, 9)
        self.assertIsNotNone(r)
        self.assertTrue(r.double_separating)
        self.assertFalse(r.double_applying)
        self.assertTrue(r.separating)
        self.assertEqual(t.motion_status(63, 0, 1, -2, 60), "Double separation")

    def test_double_application_and_separation_crossing_aries(self):
        self.assertEqual(t.motion_status(359, 1, 1, -1, 0), "Double application")
        self.assertEqual(t.motion_status(359, 1, -1, 1, 0), "Double separation")

    def test_same_direction_retrogrades_use_relative_motion(self):
        # Both retrograde bodies can still yield ordinary application or separation.
        self.assertEqual(t.motion_status(100, 193, -1, -2, 90), "Applying")
        self.assertEqual(t.motion_status(100, 193, -2, -1, 90), "Separating")

    def test_exact_stationary_and_single_application(self):
        self.assertEqual(t.motion_status(0, 60, 1, -1, 60), "Exact")
        self.assertEqual(t.motion_status(0, 63, 0, 0, 60), "Stationary")
        self.assertEqual(t.motion_status(0, 63, 2, 1, 60), "Applying")
        self.assertEqual(t.motion_status(0, 63, 1, 2, 60), "Separating")

    def test_near_exact_contact_keeps_its_direction(self):
        # A finite time step used to overshoot exactness: the Moon a few
        # arc-seconds before an exact square was reported as separating.
        for before in (0.02, 0.006, 0.001, 1e-5):
            with self.subTest(before=before):
                self.assertEqual(t.motion_status(90 - before, 0, 13.0, 0.0, 90),
                                 "Applying")
                self.assertEqual(t.motion_status(90 + before, 0, 13.0, 0.0, 90),
                                 "Separating")
        self.assertEqual(t.motion_status(180 - 1e-5, 0, 13.0, 0.0, 180),
                         "Applying")
        self.assertEqual(t.motion_status(1e-5, 0, -13.0, 0.0, 0), "Applying")

    def test_deviation_rate_is_signed_and_linear(self):
        self.assertAlmostEqual(t.deviation_rate(0, 63, 2, 0, 60), -2)
        self.assertAlmostEqual(t.deviation_rate(0, 63, 0, 2, 60), 2)
        self.assertAlmostEqual(t.deviation_rate(359, 2, 1, -1, 0), -2)
        self.assertEqual(t.deviation_rate(0, 60, 1, 0, 60), 0.0)


    def test_custom_orb_validation(self):
        values = {"aspect_preset": "custom"}
        values.update({"aspect_custom_" + name.lower(): orb
                       for name, orb in zip(t.PLANETS, t.COURSE_ORBS)})
        self.assertEqual(t.configured_orbs(values), t.COURSE_ORBS)
        values["aspect_custom_mars"] = -2
        with self.assertRaises(ValueError):
            t.configured_orbs(values)

    def test_invalid_methods(self):
        with self.assertRaises(ValueError):
            t.combine_orbs(9, -7)
        with self.assertRaises(ValueError):
            t.evaluate(0, float('nan'), 0, 0, 9, 9)


if __name__ == "__main__":
    unittest.main()
