"""Regression tests for A5 cross-chart traditional aspects and receptions."""
import unittest
from types import SimpleNamespace as NS

import crosschart_aspects as cross
from traditional_aspects import PLANETS, COURSE_ORBS


def options():
    dignities = [[[False] * 12 for _ in range(2)] for _ in range(7)]
    dignities[4][0][1] = True   # Venus owns Taurus
    dignities[2][0][0] = True   # Mars owns Aries
    dignities[1][1][3] = True   # Jupiter exalted Cancer
    return NS(
        ayanamsha=0, usedaynightorb=False, orbs=[9] * 7,
        dignities=dignities, trips=[[[0, 1, 2]] * 4], seltrip=0,
        oneruler=True, terms=[[[[1, 30]] for _ in range(12)]],
        selterm=0, decans=[[[1] * 3 for _ in range(12)]],
        seldecan=0, useexaltationmercury=False)


def chart(lons, speeds=None, ayan=0, day=True):
    speeds = [0] * 7 if speeds is None else speeds
    return NS(ayanamsha=ayan,
              planets=NS(planets=[
                  NS(data=[lon, 0, 0, speed],
                     speculums=[NS(abovehorizon=day)])
                  for lon, speed in zip(lons, speeds)]),
              abovehorizonwithorb=day)


def setup(a, b, **kwargs):
    opts = options()
    base = {'aspect_preset': 'traditional'}
    base.update(kwargs)
    return cross.analyze(a, b, opts, base)


class CrossChartAspectTests(unittest.TestCase):
    def test_cross_chart_same_named_planets_included(self):
        one = chart([0] * 7)
        two = chart([0] * 7)
        results = setup(one, two)
        self.assertEqual(len(results), 49)
        self.assertTrue(any(row.first == 'Sun' and row.second == 'Sun'
                            for row in results))

    def test_duplicate_identity_skipped(self):
        one = chart([0] * 7)
        self.assertEqual(setup(one, one), ())

    def test_larger_orb_of_the_two_planets(self):
        # Sun (15) and Venus (7) 12 degrees apart: within the Sun's orb.
        a = chart([90, 90, 90, 0, 90, 90, 90])
        b = chart([90, 90, 90, 90, 12, 90, 90])
        pred = lambda x: x.first == 'Sun' and x.second == 'Venus'
        self.assertTrue(any(pred(x) for x in setup(a, b)))
        # Venus (7) and Moon (12) 10 degrees apart: within the Moon's orb.
        c = chart([90, 90, 90, 90, 90, 90, 10])
        d = chart([90, 90, 90, 90, 0, 90, 90])
        self.assertTrue(any(x.first == 'Moon' and x.second == 'Venus'
                            for x in setup(c, d)))
        d.planets.planets[4].data[0] = 357  # 13 degrees: beyond both orbs
        self.assertFalse(any(x.first == 'Moon' and x.second == 'Venus'
                             for x in setup(c, d)))

    def test_custom_planet_orbs_used(self):
        a = chart([90, 90, 90, 0, 90, 90, 90])
        b = chart([90, 90, 90, 90, 12, 90, 90])
        opts = {'aspect_preset': 'custom'}
        opts.update({'aspect_custom_' + name.lower(): 5
                     for name in PLANETS})
        result = cross.analyze(a, b, options(), opts)
        self.assertFalse(any(r.first == 'Sun' and r.second == 'Venus'
                             for r in result))
        self.assertEqual(len(COURSE_ORBS), 7)

    def test_three_degree_rule_out_of_sign(self):
        a = chart([359] + [80] * 6)
        b = chart([80, 80, 1] + [80] * 4)
        def pair(rows):
            return [r for r in rows
                    if r.first == 'Saturn' and r.second == 'Mars']
        permitted = setup(a, b)
        self.assertEqual(len(pair(permitted)), 1)
        self.assertTrue(pair(permitted)[0].out_of_sign)
        b.planets.planets[2].data[0] = 3  # 4 degrees across the boundary
        self.assertFalse(pair(setup(a, b)))

    def test_chart_order_is_not_collapsed(self):
        a = chart([0] + [70] * 6)
        b = chart([2] + [70] * 6, speeds=[1] + [0] * 6)
        pairs = setup(a, b)
        self.assertEqual(next(r for r in pairs if r.first == 'Saturn'
                          and r.second == 'Saturn').motion_b, 'Leaving A')
        reverse = setup(b, a)
        self.assertEqual(next(r for r in reverse if r.first == 'Saturn'
                          and r.second == 'Saturn').motion_b, 'Stationary')

    def test_b_motion_only_not_natal_motion(self):
        a = chart([0] + [90] * 6,
                  speeds=[-40] + [0] * 6)
        b = chart([63] + [90] * 6,
                  speeds=[-1] + [0] * 6)
        result = setup(a, b)
        saturn = next(r for r in result
                      if r.first == 'Saturn' and r.second == 'Saturn')
        self.assertEqual(saturn.aspect, 'Sextile')
        self.assertEqual(saturn.motion_b, 'Approaching A')

    def test_motion_near_aries_wrap(self):
        a = chart([359] + [90] * 6)
        b = chart([1] + [90] * 6, speeds=[-1] + [0] * 6)
        r = next(r for r in setup(a, b)
                 if r.first == r.second == 'Saturn')
        self.assertEqual(r.motion_b, 'Approaching A')

    def test_reception_directed_venus_receives_mars(self):
        # A Venus 42 Taurus; B Mars 43 Taurus. Venus receives Mars.
        a = chart([180, 180, 180, 180, 42, 180, 180])
        b = chart([180, 180, 43, 180, 180, 180, 180])
        row = next(r for r in setup(a, b)
                   if r.first == 'Venus' and r.second == 'Mars')
        self.assertIn('domicile', row.a_receives_b)
        self.assertFalse(row.b_receives_a)

    def test_reverse_reception_host_b_receives_a(self):
        a = chart([180, 180, 12, 180, 180, 180, 180])
        b = chart([180, 180, 180, 180, 13, 180, 180])
        row = next(r for r in setup(a, b)
                   if r.first == 'Mars' and r.second == 'Venus')
        self.assertIn('domicile', row.a_receives_b)
        self.assertFalse(row.b_receives_a)
        reversed_rows = setup(b, a)
        rev = next(r for r in reversed_rows if r.first == 'Venus'
                   and r.second == 'Mars')
        self.assertIn('domicile', rev.b_receives_a)

    def test_planet_filters_independent(self):
        a, b = chart([0] * 7), chart([0] * 7)
        rows = cross.analyze(a, b, options(), {
            'aspect_preset': 'traditional'}, only_first='Sun', only_second='Moon')
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0].first, rows[0].second), ('Sun','Moon'))

    def test_sidereal_adjustment_each_chart_own_ayanamsha(self):
        opts = options()
        opts.ayanamsha = 1
        a = chart([350] + [90] * 6, ayan=20)
        b = chart([330] + [90] * 6, ayan=0)
        rows = cross.analyze(a, b, opts, {
            'aspect_preset': 'traditional'}, only_first='Saturn', only_second='Saturn')
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0].a_longitude, 330)
        self.assertAlmostEqual(rows[0].b_longitude, 330)

    def test_legacy_preserves_original_multiwheel_averaged_orb(self):
        opts = options()
        opts.orbs = [8] * 7
        a = chart([0] * 7)
        b = chart([9] * 7)
        vals = cross.analyze(a, b, opts, {'aspect_preset': 'legacy'},
                             only_first='Sun', only_second='Venus')
        self.assertEqual(vals, ())
        b.planets.planets[4].data[0] = 7
        vals = cross.analyze(a, b, opts, {'aspect_preset': 'legacy'},
                             only_first='Sun', only_second='Venus')
        self.assertEqual(len(vals), 1)

    def test_no_mutation_of_source_chart(self):
        a = chart([0] * 7)
        b = chart([1] * 7)
        prior = tuple(p.data[:] for p in b.planets.planets)
        setup(a, b)
        self.assertEqual(prior, tuple(p.data for p in b.planets.planets))


if __name__ == '__main__':
    unittest.main()
