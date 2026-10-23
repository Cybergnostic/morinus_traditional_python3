"""Chart picker policies tested without a GUI or Swiss Ephemeris."""

import unittest
import io
import os
import pickle
from unittest import mock

from multiwheel_sources import (CREATE_GROUPS, RecentNatal,
                                inner_chart_sources, merge_chart_sources,
                                recent_natal)


class MultiWheelSourcesTests(unittest.TestCase):
    def test_inner_picker_excludes_generated_return_and_transit_lists(self):
        class StubChart:
            def __init__(self, kind):
                self.htype = kind

        natal, another_natal = StubChart(0), StubChart(0)
        solar, lunar, transit = StubChart(1), StubChart(2), StubChart(4)
        explicit_file, entered = StubChart(4), StubChart(5)
        sources = inner_chart_sources(
            natal,
            [('Open', solar), ('Open', lunar), ('Open', another_natal),
             ('Open', transit), ('File', explicit_file)],
            [('Solar return', solar), ('Lunar return', lunar),
             ('Transits', transit), ('New chart', entered)], 0)
        self.assertEqual(sources, [
            ('Active', natal), ('New chart', entered),
            ('Open', another_natal), ('File', explicit_file)])

    def test_inner_picker_allows_explicit_open_in_translated_interface(self):
        class StubChart:
            htype = 4

        active, loaded = StubChart(), StubChart()
        self.assertEqual(inner_chart_sources(
            active, [], [('Datoteka', loaded)], 0,
            manual_labels=('Datoteka',)),
            [('Active', active), ('Datoteka', loaded)])

    def test_only_natal_recent_files_appear_without_loading_charts(self):
        def encoded(name, chart_type):
            return b''.join(pickle.dumps(value, protocol=2)
                            for value in (name, True, chart_type, False,
                                          1988, 6, 8, 19, 15))

        with mock.patch('builtins.open', return_value=io.BytesIO(encoded('Anna', 0))):
            self.assertEqual(recent_natal('/tmp/anna.hor', 0),
                             RecentNatal(os.path.abspath('/tmp/anna.hor'),
                                         'Anna', '1988-06-08 19:15'))
        with mock.patch('builtins.open', return_value=io.BytesIO(encoded('Anna SR', 1))):
            self.assertIsNone(recent_natal('/tmp/return.hor', 0))
        with mock.patch('builtins.open', return_value=io.BytesIO(b'not pickle')):
            self.assertIsNone(recent_natal('/tmp/invalid.hor', 0))

    def test_recent_header_never_imports_pickle_classes(self):
        class Dangerous:
            def __reduce__(self):
                return (os.system, ('true',))

        payload = pickle.dumps(Dangerous(), protocol=2)
        with mock.patch('builtins.open', return_value=io.BytesIO(payload)):
            with mock.patch('os.system', side_effect=AssertionError('executed')):
                self.assertIsNone(recent_natal('/tmp/not-a-chart.hor', 0))

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
