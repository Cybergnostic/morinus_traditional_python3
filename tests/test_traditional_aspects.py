"""Calculation-level regression tests for the optional traditional aspect engine."""
import unittest
import traditional_aspects as t


class TraditionalAspectTests(unittest.TestCase):
    def test_course_orbs(self):
        self.assertEqual(t.COURSE_ORBS, (9, 9, 8, 15, 7, 7, 12))

    def test_average_or_larger(self):
        self.assertEqual(t.combine_orbs(15, 7), 15)
        self.assertEqual(t.combine_orbs(15, 7, "average"), 11)

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
        self.assertIsNone(t.evaluate(359, 1, 0, 0, 9, 9, boundary_allowance=0))

    def test_out_of_sign_limit(self):
        self.assertIsNotNone(t.evaluate(358, 1, 0, 0, 9, 9))
        self.assertIsNone(t.evaluate(357, 1, 0, 0, 9, 9))
        self.assertIsNone(t.evaluate(358, 1, 0, 0, 9, 9, boundary_allowance=2))

    def test_average_changes_contact(self):
        self.assertIsNotNone(t.evaluate(0, 12, 0, 0, 15, 7))
        self.assertIsNone(t.evaluate(0, 12, 0, 0, 15, 7, method="average"))

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

    def test_strict_sign_mode_leaves_valid_sign_aspects(self):
        self.assertIsNotNone(t.evaluate(0, 62, 0, 0, 9, 9, boundary_allowance=0))

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
            t.combine_orbs(9, 7, "unknown")
        with self.assertRaises(ValueError):
            t.evaluate(0, 1, 0, 0, 9, 9, boundary_allowance=-1)


if __name__ == "__main__":
    unittest.main()
