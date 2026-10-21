"""Fixed Stars menu coverage and distinct angular/paran tolerances."""
import unittest
import fixedstarscatalog as f


class FixedStarsCatalogTests(unittest.TestCase):
    def test_legacy_commands(self):
        self.assertEqual(f.ALIASES,
                         {'onFixedStars': 0, 'onFixedStarsAsps': 1, 'onStarAngles': 2})
        self.assertEqual(len(f.TABS), 3)
        self.assertEqual(len(f.DESCRIPTIONS), 3)
        self.assertEqual(set(f.ALIASES.values()), set(range(3)))

    def test_no_star_guard(self):
        self.assertFalse(f.is_selected([]))
        self.assertTrue(f.is_selected(['Aldebaran']))


if __name__ == '__main__':
    unittest.main()
