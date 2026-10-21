"""Native hours-and-rise-set workspace navigation checks."""
import unittest
import hourscatalog


class HoursWorkspaceTests(unittest.TestCase):
    def test_old_menus_cover_both_tabs(self):
        self.assertTrue(hourscatalog.has_both_tables())
        self.assertEqual(hourscatalog.ALIASES['onPlanetaryHours'], 0)
        self.assertEqual(hourscatalog.ALIASES['onRiseSet'], 1)

    def test_different_techniques_keep_separate_tabs(self):
        self.assertEqual(len(set(hourscatalog.TABS)), 2)


if __name__ == '__main__':
    unittest.main()
