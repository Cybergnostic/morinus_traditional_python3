"""Tests for command discovery ranking; no wxPython or display required."""
import unittest
from commandindex import normalise, search


def command(name, where='', detail=''):
    return (name, where, detail, lambda: None)


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.cmds = [
            command('Fixed stars', 'Tables', 'Star positions'),
            command('Fixed stars on angles', 'Tables', 'Paranatellonta'),
            command('Settings', 'Settings', 'All preferences'),
            command('Star colors', 'Settings › Appearance', 'Customize star color'),
            command('Solar return', 'Charts', 'Chart return'),
            command('Lunar return', 'Charts', 'Chart return'),
        ]

    def test_empty_search(self):
        self.assertEqual(search(self.cmds, ''), [])

    def test_exact_name_first(self):
        self.assertEqual(search(self.cmds, 'fixed stars')[0][0], 'Fixed stars')

    def test_multiple_words_any_order(self):
        self.assertEqual(search(self.cmds, 'angles stars')[0][0], 'Fixed stars on angles')

    def test_help_and_menu_path(self):
        self.assertEqual(search(self.cmds, 'paranatellonta')[0][0], 'Fixed stars on angles')
        self.assertEqual(search(self.cmds, 'appearance colors')[0][0], 'Star colors')

    def test_case_accents_and_punctuation(self):
        self.assertEqual(normalise('Lúnar-Return...'), 'lunar return')
        self.assertEqual(search(self.cmds, 'LUNAR return')[0][0], 'Lunar return')

    def test_limit(self):
        self.assertEqual(len(search(self.cmds, 'return', 1)), 1)

    def test_unmatched(self):
        self.assertEqual(search(self.cmds, 'not a command'), [])


if __name__ == '__main__':
    unittest.main()
