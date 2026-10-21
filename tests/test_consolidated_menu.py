"""No duplicated menu commands after B1-B4 workspace consolidation.

Static menu-contract tests require only the stdlib; they do not import wx.
"""
import ast
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ConsolidatedMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / 'morin.py').read_text(encoding='utf-8')
        cls.selection = (ROOT / 'menuseldlg.py').read_text(encoding='utf-8')
        cls.navigator = (ROOT / 'lunationnavigator.py').read_text(encoding='utf-8')
        for source in (cls.app, cls.selection, cls.navigator):
            ast.parse(source)

    def test_one_entry_per_positions_stars_and_hours_workspace(self):
        table = self.app.split('self.mtables = wx.Menu()', 1)[1].split(
            'finish(self.mtables', 1)[0]
        for label in ('Positions and data...', 'Fixed Stars...',
                      'Planetary hours and rise/set...'):
            self.assertEqual(table.count(repr(label).strip("'")), 1)
        for old in ('TMPositions', 'TMMunPos', 'TMSpeeds', 'TMMisc',
                    'TMFixStars', 'TMFixStarsAsps',
                    'TMPlanetaryHours', 'TMRiseSet',
                    'Fixed stars on the angles'):
            self.assertNotIn("'" + old + "'", table)

    def test_only_consolidated_lunation_menu_item(self):
        charts = self.app.split('self.mcharts = wx.Menu()', 1)[1].split(
            'finish(self.mcharts', 1)[0]
        self.assertEqual(charts.count('Syzygies and lunar phases...'), 1)
        self.assertNotIn("'PMSyzygy'", charts)
        self.assertNotIn("'PMSyzygy2'", charts)

    def test_original_syzygy_chart_handlers_remain_accessible(self):
        for name in ('onSyzygyChart', 'onSyzygyChart2'):
            self.assertIn('    def ' + name + '(', self.app)
            self.assertIn('self.mainfr.' + name + ')', self.navigator)

    def test_menu_selection_persistence_slots_are_intact_but_hidden(self):
        # Slots are not deleted, because old .opt files store indexed arrays.
        tables = self.selection.split('tabtxts = (', 1)[1].split(')', 1)[0]
        charts = self.selection.split('ctxts = (', 1)[1].split(')', 1)[0]
        self.assertEqual(tables.count('mtexts.menutxts['), 22)
        self.assertEqual(charts.count('mtexts.menutxts['), 10)
        self.assertIn('HIDDEN_LEGACY_TABLES = frozenset((0, 4, 5, 9, 10, 12, 13, 16))',
                      self.selection)
        self.assertIn('HIDDEN_LEGACY_CHARTS = frozenset((6, 7))', self.selection)
        self.assertIn('if i in HIDDEN_LEGACY_TABLES:', self.selection)
        self.assertIn('if i in HIDDEN_LEGACY_CHARTS:', self.selection)


if __name__ == '__main__':
    unittest.main()
