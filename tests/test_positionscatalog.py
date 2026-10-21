"""Positions workspace navigation and method-selection contracts."""
import unittest

import positionscatalog


class PositionsCatalogTests(unittest.TestCase):
    def test_all_legacy_commands_have_independent_tab(self):
        self.assertEqual(positionscatalog.MENU_TABS,
                         {'onPositions': 1, 'onMunPos': 0, 'onSpeeds': 0, 'onMisc': 0, 'onUserSpeculum': 1})
        self.assertEqual(len(positionscatalog.TABS), 2)
        self.assertEqual(len(positionscatalog.DESCRIPTIONS), 2)
        self.assertEqual(set(positionscatalog.MENU_TABS.values()), set(range(2)))

    def test_speculum_default_follows_primary_directions(self):
        self.assertEqual(positionscatalog.initial_speculum(2, 2), 1)
        self.assertEqual(positionscatalog.initial_speculum(0, 2), 0)
        self.assertEqual(positionscatalog.initial_speculum(3, 2), 0)

    def test_speculum_selection_does_not_modify_settings(self):
        cols = [[True, False, False], [False, True, False]]
        before = [v[:] for v in cols]
        self.assertTrue(positionscatalog.has_columns(cols, 0))
        self.assertTrue(positionscatalog.has_columns(cols, 1))
        self.assertEqual(cols, before)

    def test_empty_columns_do_not_construct_empty_table(self):
        cols = [[False, False], [False, True]]
        self.assertFalse(positionscatalog.has_columns(cols, 0))
        self.assertTrue(positionscatalog.has_columns(cols, 1))
        self.assertFalse(positionscatalog.has_columns(cols, 2))
        self.assertFalse(positionscatalog.has_columns(cols, -1))


if __name__ == '__main__':
    unittest.main()
