"""Chart picker policies tested without a GUI or Swiss Ephemeris."""

import unittest

from multiwheel_sources import CREATE_GROUPS, merge_chart_sources


class MultiWheelSourcesTests(unittest.TestCase):
    def test_all_chart_sources_are_unique_by_identity(self):
        active, solar, lunar, independent = object(), object(), object(), object()
        result = merge_chart_sources(
            active,
            [('Open', solar), ('Duplicate', active), ('Open', lunar),
             ('Same chart', solar), ('None', None)],
            [('Created', lunar), ('Created', independent)])
        self.assertEqual(result, [
            ('Active', active), ('Created', lunar), ('Created', independent),
            ('Open', solar)])

    def test_unrelated_charts_with_same_value_are_independent(self):
        a = [1]
        b = [1]
        sources = merge_chart_sources(a, [('Open', b)], ())
        self.assertEqual(len(sources), 2)
        self.assertIs(sources[0][1], a)
        self.assertIs(sources[1][1], b)

    def test_create_menu_groups_only_chart_producing_actions(self):
        actions = [action for _, entries in CREATE_GROUPS
                   for _, action in entries]
        self.assertEqual(len(actions), len(set(actions)))
        self.assertEqual(set(actions), {
            'new', 'here_now', 'synastry', 'solar', 'lunar',
            'saturn', 'jupiter', 'mars', 'venus', 'mercury',
            'transits', 'sun_transits', 'secondary', 'profections',
            'elections', 'syzygy', 'syzygy_other',
        })
        self.assertGreaterEqual(len(CREATE_GROUPS), 3)
        self.assertTrue(all(entries for _, entries in CREATE_GROUPS))


if __name__ == '__main__':
    unittest.main()
