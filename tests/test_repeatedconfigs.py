"""The solar-vs-natal pattern search never requires wx or Swiss Ephemeris."""

import unittest

import repeatedconfigs as rc


NATAL = dict(zip(rc.PLANETS, (10.0, 51.0, 100.0, 145.0, 200.0, 277.0, 333.0)))
SOLAR = dict(zip(rc.PLANETS, (40.0, 73.0, 130.0, 175.0, 259.0, 312.0, 349.0)))


class RepeatedConfigTests(unittest.TestCase):
    def test_wraparound_conjunction_and_opposition(self):
        self.assertEqual(rc.configured(359.0, 1.0, 9, 9), ('Conjunction', 2.0))
        self.assertEqual(rc.configured(2.0, 181.0, 9, 9), ('Opposition', 1.0))

    def test_aspects_are_configured_by_the_course_rule(self):
        # Venus (7) and Moon (12) 10 degrees apart: within the Moon's orb.
        self.assertEqual(rc.configured(0.0, 10.0, 7, 12), ('Conjunction', 10.0))
        self.assertIsNone(rc.configured(0.0, 13.0, 7, 12))
        # Across a sign boundary only within three degrees.
        self.assertIsNone(rc.configured(357.0, 1.0, 9, 9))
        # Sidereal: the signs of the chart's own zodiac decide.
        self.assertIsNone(rc.configured(28.0, 35.0, 9, 9))
        self.assertEqual(rc.configured(28.0, 35.0, 9, 9, shift=24.0)[0], 'Conjunction')

    def test_repetition_needs_configuration_in_both_charts(self):
        natal = dict(NATAL, Venus=190.0, Moon=200.0)    # 10 apart in Libra: configured
        solar = dict(SOLAR, Venus=259.0, Moon=269.0)
        self.assertTrue(any(a.planets == ('Venus', 'Moon')
                            for a in rc.search(natal, solar).aspects))
        solar = dict(SOLAR, Venus=259.0, Moon=272.0)    # 13 apart: not
        self.assertFalse(any(a.planets == ('Venus', 'Moon')
                             for a in rc.search(natal, solar).aspects))

    def test_same_named_pair_same_aspect_both_charts(self):
        found = rc.search(NATAL, SOLAR, 5.0, year_lord='Mars')
        squares = [a for a in found.aspects if a.planets == ('Saturn', 'Mars')]
        self.assertEqual(len(squares), 1)
        self.assertEqual(squares[0].aspect, 'Square')
        self.assertTrue(squares[0].involves_year_lord)

    def test_different_aspect_is_not_repeated(self):
        solar = dict(SOLAR, Mars=160.0)  # Saturn-Mars becomes a trine
        found = rc.search(NATAL, solar, 5.0)
        self.assertFalse(any(a.planets == ('Saturn', 'Mars') for a in found.aspects))

    def test_both_orbs_must_be_inside_the_limit(self):
        natal = dict(NATAL, Mars=101.0)
        solar = dict(SOLAR, Mars=136.0)
        self.assertFalse(any(a.planets == ('Saturn', 'Mars')
                             for a in rc.search(natal, solar, 5.0).aspects))
        self.assertTrue(any(a.planets == ('Saturn', 'Mars')
                            for a in rc.search(natal, solar, 6.0).aspects))

    def test_repeating_three_planet_configuration(self):
        natal = dict(NATAL, Saturn=0.0, Jupiter=120.0, Mars=240.0)
        solar = dict(SOLAR, Saturn=12.0, Jupiter=132.0, Mars=252.0)
        found = rc.search(natal, solar, year_lord='Saturn')
        rows = [r for r in found.triples if r.planets == ('Saturn', 'Jupiter', 'Mars')]
        self.assertEqual(len(rows), 1)
        self.assertEqual(tuple(a.aspect for a in rows[0].relations), ('Trine',) * 3)
        self.assertTrue(rows[0].involves_year_lord)

    def test_partial_triangle_not_reported(self):
        natal = dict(NATAL, Saturn=0.0, Jupiter=120.0, Mars=240.0)
        solar = dict(SOLAR, Saturn=12.0, Jupiter=132.0, Mars=275.0)
        found = rc.search(natal, solar)
        self.assertNotIn(('Saturn', 'Jupiter', 'Mars'), [t.planets for t in found.triples])

    def test_annual_lord_filter_on_pairs_and_triples(self):
        natal = dict(NATAL, Saturn=0.0, Jupiter=120.0, Mars=240.0)
        solar = dict(SOLAR, Saturn=12.0, Jupiter=132.0, Mars=252.0)
        found = rc.search(natal, solar, year_lord='Saturn', annual_only=True)
        self.assertTrue(all('Saturn' in a.planets for a in found.aspects))
        self.assertTrue(any(t.planets == ('Saturn', 'Jupiter', 'Mars') for t in found.triples))

    def test_sidereal_sign_and_whole_sign_house_positions(self):
        natal = dict(NATAL, Mercury=34.0, Moon=145.0, Sun=10.0)
        solar = dict(SOLAR, Mercury=65.0, Moon=265.0, Sun=10.0)
        found = rc.search(natal, solar, include_placements=True,
                          natal_asc=12.0, solar_asc=120.0,
                          natal_ayanamsha=0.0, solar_ayanamsha=30.0)
        self.assertIn(('Mercury', 'Sign', 1), [(p.planet, p.kind, p.index)
                                             for p in found.placements])
        self.assertNotIn(('Sun', 'Sign', 0), [(p.planet, p.kind, p.index)
                                            for p in found.placements])

    def test_repeated_whole_sign_house(self):
        natal = dict(NATAL, Moon=145.0)
        solar = dict(SOLAR, Moon=265.0)
        found = rc.search(natal, solar, include_placements=True,
                          natal_asc=12.0, solar_asc=120.0)
        self.assertIn(('Moon', 'Whole-sign house', 5),
                      [(p.planet, p.kind, p.index) for p in found.placements])

    def test_input_validation(self):
        with self.assertRaisesRegex(ValueError, 'Missing natal'):
            rc.search({}, SOLAR)
        with self.assertRaisesRegex(ValueError, 'Maximum deviation'):
            rc.search(NATAL, SOLAR, float('nan'))
        with self.assertRaisesRegex(ValueError, 'required'):
            rc.search(NATAL, SOLAR, annual_only=True)
        with self.assertRaisesRegex(ValueError, 'Ascendants'):
            rc.search(NATAL, SOLAR, include_placements=True)


if __name__ == '__main__':
    unittest.main()
