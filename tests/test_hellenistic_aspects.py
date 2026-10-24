"""A4 regression tests: sign aversion, shared rulership, mirror points and rays."""
import unittest
from types import SimpleNamespace

from hellenistic_aspects import (
    analyze_aversions, analyze_rays, directed_ray, overcomes,
    signs_averse, _reflections,
)
from light_perfection import Connection


def chart(lons=None, speeds=None, asc=45, contacts=(), ayan=0):
    lons = lons if lons is not None else [5, 105, 273, 235, 195, 70, 300]
    speeds = speeds if speeds is not None else [0, 0, 1, .9, 1, 1, 12]
    ps = [SimpleNamespace(data=[lon, 0, 0, speed])
          for lon, speed in zip(lons, speeds)]
    matrix = [[SimpleNamespace(typ=-1) for j in range(9)]
              for i in range(9)]
    for first, second, kind in contacts:
        matrix[max(first, second)][min(first, second)].typ = kind
    return SimpleNamespace(
        planets=SimpleNamespace(planets=ps),
        houses=SimpleNamespace(ascmc=[asc]),
        options=SimpleNamespace(ayanamsha=1 if ayan else 0),
        ayanamsha=ayan, aspmatrix=matrix)


class A4GeometryTests(unittest.TestCase):
    def test_aversion_second_sixth_eighth_twelfth(self):
        self.assertTrue(all(signs_averse(0, other) for other in (1, 5, 7, 11)))
        self.assertFalse(any(signs_averse(0, other)
                             for other in (0, 2, 3, 4, 6, 8, 9, 10)))

    def test_direction_is_from_the_named_caster(self):
        self.assertEqual(directed_ray(0, 9), ('Square', 'Dexter'))
        self.assertEqual(directed_ray(9, 0), ('Square', 'Sinister'))
        self.assertEqual(directed_ray(0, 3), ('Square', 'Sinister'))
        self.assertEqual(directed_ray(3, 0), ('Square', 'Dexter'))
        self.assertIsNone(directed_ray(0, 6))

    def test_overcoming_not_same_as_dexter(self):
        self.assertTrue(overcomes(9, 0))   # Capricorn in tenth from Aries
        self.assertFalse(overcomes(0, 9))
        self.assertTrue(overcomes(8, 0))
        self.assertTrue(overcomes(10, 0))
        self.assertFalse(overcomes(0, 6))

    def test_venus_libra_taurus_ascendant_shared_ruler(self):
        ch = chart()
        rows = [r for r in analyze_aversions(ch)
                if r.scope == 'Ascendant' and r.source == 'Venus']
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].source_sign, 'Libra')
        self.assertEqual(rows[0].target_sign, 'Taurus')
        self.assertEqual(rows[0].geometry, 'Averse')
        self.assertEqual(rows[0].condition, 'Mitigated')
        self.assertIn('Common domicile ruler: Venus', rows[0].mitigations)

    def test_other_domicile_of_same_planet_is_mitigated(self):
        ch = chart()
        rows = [r for r in analyze_aversions(ch)
                if r.scope == 'Ruler to domicile' and
                r.source == 'Venus' and r.target == 'Taurus domicile']
        self.assertEqual(len(rows), 1)
        self.assertIn('Common domicile ruler: Venus', rows[0].mitigations)

    def test_antiscia_sign_and_degree_distinction(self):
        # Aries 14.25 -> Virgo 15.75 by solstice reflection.
        methods = _reflections(14.25, 165.75)
        self.assertIn('Antiscia (sign)', methods)
        self.assertIn('Antiscia (degree)', methods)
        self.assertNotIn('Contra-antiscia (sign)', methods)

    def test_antiscia_sign_without_degree_proximity(self):
        methods = _reflections(2, 150)
        self.assertIn('Antiscia (sign)', methods)
        self.assertNotIn('Antiscia (degree)', methods)

    def test_contra_antiscia_sign_pairing(self):
        # Aries and Pisces are contra-antiscia signs.
        methods = _reflections(15, 345)
        self.assertIn('Contra-antiscia (sign)', methods)
        self.assertNotIn('Antiscia (sign)', methods)

    def test_light_mitigation_only_after_a3_verification(self):
        ch = chart(lons=[5, 105, 273, 235, 195, 70, 300], asc=12)
        # Saturn in Aries, Moon in Aquarius: sign sextile, choose instead
        # Saturn in Aries, Venus in Libra? opposition. Saturn -> Jupiter in
        # Cancer is square. Pick Saturn in Aries and Mercury in Gemini:
        # sextile. Averse planet pair: Saturn Aries and Venus in Virgo.
        ch.planets.planets[4].data[0] = 165.5
        links = [Connection('Translation', 'Moon', 'Saturn', 'Venus',
                            'Sextile', 'Trine', 'Candidate')]
        pair = lambda rr: next(r for r in rr
                               if r.scope == 'Planet pair' and
                               {r.source, r.target} == {'Saturn', 'Venus'})
        self.assertFalse(any('Translation' in s
                   for s in pair(analyze_aversions(ch, links)).mitigations))
        links = [Connection('Translation', 'Moon', 'Saturn', 'Venus',
                            'Sextile', 'Trine', 'Verified')]
        self.assertIn('Translation via Moon',
                      pair(analyze_aversions(ch, links)).mitigations)

    def test_sidereal_sign_adjustment(self):
        # Tropical Libra Venus -> Virgo after 30 degree ayanamsha,
        # Aries Ascendant -> Pisces.
        ch = chart(lons=[5, 105, 273, 235, 195, 70, 300],
                   asc=45, ayan=30)
        venus = next(r for r in analyze_aversions(ch)
                     if r.scope == 'Ascendant' and r.source == 'Venus')
        self.assertEqual(venus.source_sign, 'Virgo')
        self.assertEqual(venus.target_sign, 'Aries')


class A4RaysTests(unittest.TestCase):
    def test_named_direction_and_overcoming(self):
        # Mars 273 Capricorn overcomes Saturn 5 Aries by sinister square.
        ch = chart(contacts=[(0, 2, 2)])
        rows = analyze_rays(ch)
        mars = next(r for r in rows if r.caster == 'Mars'
                    and r.target == 'Saturn')
        self.assertEqual(mars.direction, 'Sinister')
        self.assertEqual(mars.aspect, 'Square')
        self.assertEqual(mars.overcoming, 'Yes')
        self.assertEqual(mars.degree_orb, 2.0)
        self.assertTrue(mars.close_counter_ray)
        self.assertTrue(mars.aktinobolia)
        saturn = next(r for r in rows if r.caster == 'Saturn'
                      and r.target == 'Mars')
        self.assertEqual(saturn.direction, 'Dexter')
        self.assertEqual(saturn.overcoming, 'No')

    def test_no_aktinobolia_when_overcomer_is_separating(self):
        ch = chart(speeds=[0, 0, -1, .9, 1, 1, 12],
                   contacts=[(0, 2, 2)])
        r = next(r for r in analyze_rays(ch)
                 if r.caster == 'Mars' and r.target == 'Saturn')
        self.assertTrue(r.close_counter_ray)
        self.assertFalse(r.aktinobolia)

    def test_sign_based_ray_exists_outside_degree_orb(self):
        ch = chart(lons=[20, 105, 270, 235, 195, 70, 300])
        r = next(r for r in analyze_rays(ch)
                 if r.caster == 'Mars' and r.target == 'Saturn')
        self.assertEqual(r.overcoming, 'Yes')
        self.assertFalse(r.in_orb)
        self.assertFalse(r.aktinobolia)

    def test_averse_planet_pair_has_no_ray(self):
        ch = chart(lons=[5, 105, 273, 235, 165, 70, 300])
        rays = analyze_rays(ch)
        self.assertFalse(any({r.caster, r.target} == {'Saturn','Venus'}
                             for r in rays))


if __name__ == '__main__':
    unittest.main()
