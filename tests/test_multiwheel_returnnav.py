import unittest
from types import SimpleNamespace

from multiwheel_returnnav import (
    linked_lunar_indices, match_return_index, nearest_inner_solar,
    next_return_index, solar_year_window)


class ReturnNavigationTests(unittest.TestCase):
    def test_solar_year_window(self):
        self.assertEqual(solar_year_window(2026), (2024, 2025, 2026, 2027, 2028))
        self.assertEqual(solar_year_window(1), (1, 2, 3))

    def test_link_only_the_same_natal_and_only_outer_rings(self):
        natal_a, natal_b = object(), object()
        assignments = [
            (None, None), ('solar', natal_a), ('lunar', natal_a),
            ('lunar', natal_b),
        ]
        self.assertEqual(nearest_inner_solar(2, assignments), 1)
        self.assertIsNone(nearest_inner_solar(3, assignments))
        self.assertEqual(linked_lunar_indices(1, assignments), (2,))
        self.assertEqual(linked_lunar_indices(0, assignments), ())

    def test_nearest_matching_solar_wins_without_explicit_toggle(self):
        natal = object()
        assignments = [
            ('solar', natal), ('solar', natal), ('lunar', natal),
        ]
        self.assertEqual(nearest_inner_solar(2, assignments), 1)
        self.assertEqual(linked_lunar_indices(0, assignments), ())

    def test_unknown_origin_never_auto_links(self):
        assignments = [('solar', None), ('lunar', None)]
        self.assertIsNone(nearest_inner_solar(1, assignments))
        self.assertEqual(linked_lunar_indices(0, assignments), ())

    def test_find_lunar_in_force_and_skip_duplicate_across_years(self):
        old = [SimpleNamespace(jd=jd) for jd in (100., 130., 160.)]
        new = [SimpleNamespace(jd=jd) for jd in (160., 190., 220.)]
        self.assertEqual(match_return_index(new, 160.001), 0)
        self.assertEqual(next_return_index(new, 160., True), 1)
        self.assertEqual(next_return_index(old, 160., False), 1)
        self.assertIsNone(next_return_index(old, 160., True))
        self.assertIsNone(next_return_index(new, 160., False))


if __name__ == '__main__':
    unittest.main()
