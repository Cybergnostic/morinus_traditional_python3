"""Pure search-navigation tests for the Settings window (no GUI required)."""
import unittest
from settingsindex import categories, label, search


def rec(title, category, description, group='', index=0):
    return {'title': title, 'category': category, 'description': description,
            'group': group, 'category_index': index, 'control': None}


class SettingsSearchTests(unittest.TestCase):
    def setUp(self):
        self.data = [
            rec('Terms', 'Dignities', 'Egyptian, Ptolemaic, or edited bounds', index=3),
            rec('House system', 'Calculation', 'Regiomontanus, Whole Sign, Alcabitius', index=2),
            rec('Length of a year', 'Time lords', '360 days (Valens), solar year',
                group='Zodiacal releasing', index=6),
            rec('Years shown', 'Time lords', 'How many years after birth',
                group='Decennials', index=6),
            rec('Years shown', 'Time lords', 'How many years after birth',
                group='Zodiacal releasing', index=6),
            rec('GeoNames user name', 'Places and time zones', 'Online atlas search',
                group='Places and time zones', index=8),
        ]

    def test_egyptian_terms(self):
        self.assertEqual(search(self.data, 'Egyptian terms')[0]['title'], 'Terms')

    def test_exact_control(self):
        self.assertEqual(search(self.data, 'Regiomontanus')[0]['title'], 'House system')

    def test_individual_field_with_group(self):
        self.assertEqual(search(self.data, 'zodiacal releasing length')[0]['title'], 'Length of a year')

    def test_multiple_same_named_settings(self):
        hits = search(self.data, 'years shown')
        self.assertEqual(len(hits), 2)
        self.assertNotEqual(label(hits[0]), label(hits[1]))

    def test_empty_unmatched_and_case(self):
        self.assertEqual(search(self.data, ''), [])
        self.assertEqual(search(self.data, 'nonsense'), [])
        self.assertEqual(search(self.data, 'EGYPTIAN TERMS')[0]['title'], 'Terms')

    def test_categories(self):
        rows = categories([('General', []), ('Dignities', [])])
        self.assertEqual([r['category_index'] for r in rows], [0, 1])
        self.assertTrue(all(r['control'] is None for r in rows))


if __name__ == '__main__':
    unittest.main()
